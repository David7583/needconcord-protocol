"""Reproducible synthetic two-process loopback evidence; no real organizations."""
import argparse
import hashlib
import http.client
import json
import os
from pathlib import Path
import secrets
import socket
import sqlite3
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from odip.node import ENDPOINT
from odip.validation import encode


def port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def request(port_number, token, raw, *, auth=True):
    conn = http.client.HTTPConnection("127.0.0.1", port_number, timeout=4)
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = "Bearer " + token
    try:
        conn.request("POST", ENDPOINT, raw, headers)
        response = conn.getresponse()
        return response.status, json.loads(response.read())
    finally:
        conn.close()


class Harness:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.ports = {"a": port(), "b": port()}
        while self.ports["a"] == self.ports["b"]:
            self.ports["b"] = port()
        self.token = secrets.token_hex(32)
        self.processes, self.logs, self.events = {}, {}, []
        self.ids = {"a": "test-node-a", "b": "test-node-b"}
        for node, other in [("a", "b"), ("b", "a")]:
            config = {"participant_id": self.ids[node], "peers": {self.ids[other]: {"url": f"http://127.0.0.1:{self.ports[other]}", "token": self.token}}, "selected_recipients": [self.ids[other]]}
            (self.folder / f"{node}.local.json").write_text(json.dumps(config), encoding="utf-8")

    def command(self, node, command, *extra):
        return [sys.executable, "-m", "odip.node", command, "--config", str(self.folder / f"{node}.local.json"), "--db", str(self.folder / f"{node}.sqlite3"), *extra]

    def start(self, node):
        log = (self.folder / f"{node}.log").open("a", encoding="utf-8")
        self.logs[node] = log
        process = subprocess.Popen(self.command(node, "serve", "--port", str(self.ports[node])), cwd=ROOT, stdout=log, stderr=log,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        self.processes[node] = process
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError((self.folder / f"{node}.log").read_text(encoding="utf-8"))
            conn = http.client.HTTPConnection("127.0.0.1", self.ports[node], timeout=.2)
            try:
                conn.request("GET", "/health")
                response = conn.getresponse()
                info = json.loads(response.read())
                if info["participant_id"] == self.ids[node]:
                    self.events.append({"event": "start", "node": node, "pid": info["pid"], "launcher_pid": process.pid, "port": self.ports[node], "database": f"{node}.sqlite3"})
                    return
            except (OSError, http.client.HTTPException):
                time.sleep(.05)
            finally:
                conn.close()
        raise RuntimeError("Node startup timeout")

    def stop(self, node):
        process = self.processes.pop(node, None)
        if process is not None:
            if process.poll() is None:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    process.terminate()
            process.wait(timeout=5)
            self.logs.pop(node).close()
            self.events.append({"event": "stop", "node": node, "pid": process.pid})

    def close(self):
        for node in list(self.processes):
            self.stop(node)

    def cli(self, node, command, *extra):
        result = subprocess.run(self.command(node, command, *extra), cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=12)
        if result.returncode not in {0, 2}:
            raise RuntimeError(result.stderr)
        return json.loads(result.stdout)

    def packet(self, example, node):
        packet = json.loads((ROOT / "examples" / example).read_text(encoding="utf-8"))
        packet["sender"] = {"participant_id": self.ids[node]}
        return packet

    def send(self, node, other, packet):
        path = self.folder / f"{packet['message_id']}.json"
        path.write_bytes(encode(packet))
        result = self.cli(node, "send", "--peer", self.ids[other], "--message", str(path))
        self.events.append({"event": "send", "from": node, "to": other, "type": packet["message_type"], "message_id": packet["message_id"], "wire_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "result": result})
        return result


def run_demo(folder, report=None):
    h = Harness(folder)
    try:
        h.start("a")
        h.start("b")
        assert h.processes["a"].pid != h.processes["b"].pid
        intent = h.packet("intent.publish.json", "a")
        assert h.send("a", "b", intent)["status"] == "accepted"
        assert h.send("a", "b", intent)["status"] == "duplicate"
        conflict = json.loads(json.dumps(intent))
        conflict["payload"]["desired_outcome"] += " (conflict)"
        status, rejected = request(h.ports["b"], h.token, encode(conflict))
        assert status == 409 and rejected["payload"]["reason_code"] == "ID_CONFLICT"
        h.events.append({"event": "conflicting-replay", "http_status": status, "result": rejected})
        for name in ["proposal.goods.json", "proposal.nontransaction.json"]:
            assert h.send("b", "a", h.packet(name, "b"))["status"] == "accepted"
        assert h.send("a", "b", h.packet("outcome.no_purchase.json", "a"))["status"] == "accepted"
        # Network failure leaves durable outbox. A separate delivery loses the ACK.
        h.stop("b")
        capability = h.packet("capability.transport.json", "a")
        capability["message_id"] = str(uuid.uuid4())
        assert h.send("a", "b", capability)["status"] == "pending"
        h.start("b")
        # Simulate response loss: write raw request and close without reading any ACK.
        raw = encode(capability)
        with socket.create_connection(("127.0.0.1", h.ports["b"]), timeout=3) as conn:
            headers = f"POST {ENDPOINT} HTTP/1.1\r\nHost: 127.0.0.1\r\nAuthorization: Bearer {h.token}\r\nContent-Type: application/json\r\nContent-Length: {len(raw)}\r\nConnection: close\r\n\r\n".encode()
            conn.sendall(headers + raw)
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            with sqlite3.connect(h.folder / "b.sqlite3") as db:
                received = db.execute("SELECT COUNT(*) FROM messages WHERE id=?", (capability["message_id"],)).fetchone()[0]
            if received:
                break
            time.sleep(.05)
        assert received == 1
        h.events.append({"event": "ack-loss-injected", "message_id": capability["message_id"], "persisted_at_receiver": True})
        h.stop("b")
        h.start("b")
        retried = h.cli("a", "retry")
        assert len(retried) == 1 and retried[0]["status"] == "duplicate"
        h.events.append({"event": "retry-after-restart", "results": retried})
        assert h.send("a", "b", intent)["status"] == "duplicate"
        with sqlite3.connect(h.folder / "a.sqlite3") as a, sqlite3.connect(h.folder / "b.sqlite3") as b:
            a_id = a.execute("SELECT value FROM metadata WHERE key='participant'").fetchone()[0]
            b_id = b.execute("SELECT value FROM metadata WHERE key='participant'").fetchone()[0]
            assert a_id != b_id
            counts = {"a": a.execute("SELECT COUNT(*) FROM messages").fetchone()[0], "b": b.execute("SELECT COUNT(*) FROM messages").fetchone()[0]}
            pending = a.execute("SELECT COUNT(*) FROM outbox WHERE state='pending'").fetchone()[0]
            assert pending == 0
        h.events.append({"event": "independent-storage", "participants": [a_id, b_id], "message_counts": counts, "pending": pending})
    finally:
        h.close()
    evidence = {"synthetic": True, "transport": "loopback HTTP serialized UTF-8 JSON", "cross_implementation_verified": False, "production_security_verified": False, "passed": True, "events": h.events,
                "node_logs": {node: (h.folder / f"{node}.log").read_text(encoding="utf-8").splitlines() for node in ("a", "b")}}
    if report:
        Path(report).parent.mkdir(parents=True, exist_ok=True)
        Path(report).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", required=True, help="Fresh private test directory; contains ephemeral credentials")
    parser.add_argument("--report", default="reports/two-process-evidence.json")
    args = parser.parse_args()
    path = Path(args.work_dir)
    if path.exists() and any(path.iterdir()):
        parser.error("Use an empty work directory to isolate this run")
    result = run_demo(path, args.report)
    print(json.dumps({"passed": result["passed"], "report": args.report, "synthetic": True}))
