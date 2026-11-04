"""Loopback-only HTTP test node. Pairwise random tokens are NOT production identity."""
import argparse
import hmac
import http.client
import json
import os
import socket
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from . import PROTOCOL
from .store import Store
from .validation import MAX_BYTES, Rejection, decode, encode, validate, validator

ENDPOINT = "/odip/v0.1/messages"
READ_TIMEOUT = 2.0
MAX_WORKERS = 8
RATE_PER_MINUTE = 120


def local_url(url):
    p = urlsplit(url)
    if p.scheme != "http" or p.hostname != "127.0.0.1" or p.username or p.password or p.query or p.fragment or p.path not in ("", "/"):
        raise ValueError("Only http://127.0.0.1:port loopback base URLs are allowed")
    if p.port is None or not 1 <= p.port <= 65535:
        raise ValueError("Explicit port is required")
    return p


def load_config(path):
    config = decode(Path(path).read_bytes())
    if not isinstance(config, dict) or not isinstance(config.get("participant_id"), str) or not config["participant_id"]:
        raise ValueError("participant_id required")
    peers = config.get("peers", {})
    tokens = []
    for name, peer in peers.items():
        if name == config["participant_id"]:
            raise ValueError("Peer must be a different participant")
        local_url(peer["url"])
        token = peer["token"]
        if not isinstance(token, str) or len(token) < 32 or not token.isascii() or not token.isalnum():
            raise ValueError("Use a random ASCII alphanumeric test token of at least 32 characters")
        tokens.append(token)
    if len(tokens) != len(set(tokens)):
        raise ValueError("Each peer must have a distinct token")
    if not set(config.get("selected_recipients", [])) <= set(peers):
        raise ValueError("selected_recipients must name configured peers")
    return config


def receipt(sender, original_id, status, code=None):
    p = {"original_message_id": original_id, "status": status}
    if code:
        p["reason_code"] = code
    return {"protocol": PROTOCOL, "message_id": str(uuid.uuid4()), "message_type": "receipt.ack",
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z"),
            "sender": {"participant_id": sender}, "payload": p}


class NodeServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 8
    def __init__(self, port, config, db):
        validator()  # Fail closed before binding if date-time checks are missing.
        self.config = config
        self.store = Store(db, config["participant_id"])
        self.slots = threading.BoundedSemaphore(MAX_WORKERS)
        self.rate_lock = threading.Lock()
        self.rates = {}
        super().__init__(("127.0.0.1", port), Handler)

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            request.close()
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def rate(self, principal):
        now = time.monotonic()
        with self.rate_lock:
            times = [t for t in self.rates.get(principal, []) if t > now - 60]
            if len(times) >= RATE_PER_MINUTE:
                raise Rejection("RATE_LIMIT")
            self.rates[principal] = times + [now]

    def handle_error(self, request, client_address):
        # Never print request contents or credential-bearing tracebacks.
        print(json.dumps({"event": "connection_error", "code": "INTERNAL_ERROR"}), flush=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "ODIP-Loopback-Experimental"
    sys_version = ""

    def setup(self):
        self.request.settimeout(READ_TIMEOUT)
        super().setup()

    def log_message(self, *args):
        pass

    def reply(self, status, data):
        raw = encode(data)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        try:
            self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            pass

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, {"experimental": True, "participant_id": self.server.config["participant_id"], "pid": os.getpid()})
        else:
            self.reply(404, {"error": {"code": "NOT_FOUND", "reason": "Unknown path"}})

    def do_POST(self):
        packet = None
        try:
            if self.path != ENDPOINT:
                raise Rejection("NOT_FOUND")
            auth = self.headers.get_all("Authorization", [])
            if len(auth) != 1 or not auth[0].startswith("Bearer "):
                raise Rejection("AUTH_REQUIRED")
            token = auth[0][7:]
            if not token.isascii():
                raise Rejection("AUTH_REQUIRED")
            principal = next((name for name, peer in self.server.config["peers"].items() if hmac.compare_digest(token, peer["token"])), None)
            if principal is None:
                raise Rejection("AUTH_REQUIRED")
            self.server.rate(principal)
            if self.headers.get_all("Transfer-Encoding") or self.headers.get_all("Content-Encoding"):
                raise Rejection("UNSUPPORTED_ENCODING")
            if self.headers.get("Content-Type", "").lower() not in {"application/json", "application/json; charset=utf-8"}:
                raise Rejection("CONTENT_TYPE")
            lengths = self.headers.get_all("Content-Length", [])
            if len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].isdigit():
                raise Rejection("CONTENT_LENGTH")
            if len(lengths[0]) > 8 or int(lengths[0]) > MAX_BYTES:
                raise Rejection("MESSAGE_TOO_LARGE")
            raw = self.rfile.read(int(lengths[0]))
            if len(raw) != int(lengths[0]):
                raise Rejection("INVALID_JSON")
            packet = decode(raw)
            status, packet = self.server.store.accept(raw, principal)
            ack = receipt(self.server.config["participant_id"], packet["message_id"], status)
            self.reply(200, ack)
            print(json.dumps({"event": "receive", "message_id": packet["message_id"], "type": packet["message_type"], "status": status}), flush=True)
        except (socket.timeout, TimeoutError):
            self.reply(408, {"error": {"code": "TIMEOUT", "reason": "Request body timeout"}})
        except Rejection as exc:
            body = {"error": {"code": exc.code, "reason": exc.reason}}
            if isinstance(packet, dict):
                try:
                    original_id = str(uuid.UUID(packet.get("message_id", "")))
                    if original_id != packet.get("message_id"):
                        raise ValueError()
                    body = receipt(self.server.config["participant_id"], original_id, "rejected", exc.code)
                except (ValueError, TypeError, AttributeError):
                    pass
            status = {"AUTH_REQUIRED": 401, "FORBIDDEN": 403, "PRIVACY_DENIED": 403, "NOT_FOUND": 404, "ID_CONFLICT": 409, "MESSAGE_TOO_LARGE": 413, "RATE_LIMIT": 429}.get(exc.code, 400)
            self.reply(status, body)
            print(json.dumps({"event": "reject", "code": exc.code}), flush=True)


def deliver(store, config, peer_id, raw, timeout=2):
    packet = decode(raw)
    message_id = packet["message_id"]
    try:
        if peer_id not in config["peers"]:
            raise Rejection("UNKNOWN_PEER")
        store.authorize_outbound(raw, peer_id, selected=config.get("selected_recipients", []))
    except Rejection as exc:
        # Policy changes are not transient network failures. Require explicit
        # operator review/send after restoring authority; retry skips blocked.
        store.delivery(message_id, peer_id, "blocked", exc.code)
        return {"status": "blocked", "code": exc.code, "message_id": message_id}
    peer = config["peers"][peer_id]
    p = local_url(peer["url"])
    connection = http.client.HTTPConnection("127.0.0.1", p.port, timeout=timeout)
    try:
        connection.request("POST", ENDPOINT, body=raw, headers={"Authorization": "Bearer " + peer["token"], "Content-Type": "application/json"})
        response = connection.getresponse()
        reply_raw = response.read(MAX_BYTES + 1)
        if response.status >= 500 or response.status in {408, 429}:
            raise Rejection("REMOTE_RETRYABLE")
        try:
            reply = decode(reply_raw)
        except Rejection as exc:
            raise Rejection("INVALID_RECEIPT") from exc
        if isinstance(reply, dict) and "error" in reply:
            error = reply["error"]
            if (not 400 <= response.status < 500 or set(reply) != {"error"}
                    or not isinstance(error, dict) or set(error) != {"code", "reason"}
                    or not all(isinstance(error.get(key), str) and error[key].strip() for key in ("code", "reason"))):
                raise Rejection("INVALID_RECEIPT")
            code = error["code"]
            # These errors occur before a packet can be admitted/correlated.
            # Business rejections of a parsed message require a rejected ACK.
            transport_status = {"AUTH_REQUIRED": 401, "NOT_FOUND": 404,
                                "MESSAGE_TOO_LARGE": 413, "UNSUPPORTED_ENCODING": 400,
                                "CONTENT_TYPE": 400, "CONTENT_LENGTH": 400,
                                "INVALID_JSON": 400, "DEPTH_LIMIT": 400}
            if transport_status.get(code) != response.status:
                raise Rejection("INVALID_RECEIPT")
            store.delivery(message_id, peer_id, "rejected", code)
            return {"status": "rejected", "code": code, "message_id": message_id}
        try:
            validate(reply)
        except Rejection as exc:
            raise Rejection("INVALID_RECEIPT") from exc
        if reply["message_type"] != "receipt.ack" or reply["payload"]["original_message_id"] != message_id or reply["sender"]["participant_id"] != peer_id:
            raise Rejection("INVALID_RECEIPT")
        ack_status = reply["payload"]["status"]
        if ((ack_status in {"accepted", "duplicate"} and response.status != 200)
                or (ack_status == "rejected" and not 400 <= response.status < 500)):
            raise Rejection("INVALID_RECEIPT")
        try:
            store.accept(reply_raw, peer_id)
        except Rejection as exc:
            raise Rejection("INVALID_RECEIPT") from exc
        code = reply["payload"].get("reason_code", "OK")
        store.delivery(message_id, peer_id, "rejected" if ack_status == "rejected" else "delivered", code)
        return {"status": ack_status, "code": code, "message_id": message_id, "receipt": reply}
    except (OSError, http.client.HTTPException, Rejection) as exc:
        code = exc.code if isinstance(exc, Rejection) else "TIMEOUT" if isinstance(exc, TimeoutError) else "CONNECTION_FAILED"
        store.delivery(message_id, peer_id, "pending", code)
        return {"status": "pending", "code": code, "message_id": message_id}
    finally:
        connection.close()


def send(store, config, peer, raw, timeout=2):
    if peer not in config["peers"]:
        raise Rejection("UNKNOWN_PEER")
    store.accept(raw, config["participant_id"], outgoing=True, peer=peer, selected=config.get("selected_recipients", []))
    return deliver(store, config, peer, raw, timeout)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["serve", "send", "retry", "export"])
    parser.add_argument("--config", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--port", type=int, default=8761)
    parser.add_argument("--peer")
    parser.add_argument("--message")
    parser.add_argument("--output")
    parser.add_argument("--timeout", type=float, default=2)
    args = parser.parse_args(argv)
    if not 0 < args.timeout <= 10:
        parser.error("timeout must be in (0, 10]")
    config = load_config(args.config)
    if args.command == "serve":
        server = NodeServer(args.port, config, args.db)
        print(json.dumps({"event": "listening", "pid": os.getpid(), "host": "127.0.0.1", "port": server.server_port, "participant_id": config["participant_id"], "test_identity_only": True}), flush=True)
        try:
            server.serve_forever(poll_interval=0.1)
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return 0
    store = Store(args.db, config["participant_id"])
    try:
        if args.command == "send":
            if not args.peer or not args.message:
                parser.error("send requires --peer and --message")
            result = send(store, config, args.peer, Path(args.message).read_bytes(), args.timeout)
            print(json.dumps(result, ensure_ascii=False))
            return 0 if result["status"] in {"accepted", "duplicate"} else 2
        if args.command == "retry":
            results = [deliver(store, config, item["peer"], item["raw"], args.timeout) for item in store.pending()]
            print(json.dumps(results, ensure_ascii=False))
            return 0 if all(r["status"] in {"accepted", "duplicate"} for r in results) else 2
        if not args.output:
            parser.error("export requires --output; contains authorized local data, protect the output")
        # Explicit local operator action only; no unauthenticated network export.
        with Path(args.output).open("x", encoding="utf-8") as f:
            f.write(encode(store.export()).decode("utf-8") + "\n")
        return 0
    except Rejection as exc:
        print(json.dumps({"status": "rejected", "code": exc.code}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
