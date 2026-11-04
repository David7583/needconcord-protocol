import json
import socket
import sqlite3
import threading
import time
import uuid

import pytest

from odip.node import ENDPOINT, deliver, local_url
from odip.store import Store
from odip.validation import encode
from reference.two_process_demo import Harness, request, run_demo


def test_two_process_restart_and_response_loss(tmp_path):
    evidence = run_demo(tmp_path / "two-process")
    starts = [e for e in evidence["events"] if e["event"] == "start"]
    assert len(starts) == 4
    assert starts[0]["pid"] != starts[1]["pid"]
    assert evidence["passed"]


@pytest.mark.parametrize("url", ["http://0.0.0.0:8080", "https://127.0.0.1:8080", "http://localhost:8080", "http://example.com:80", "http://127.0.0.1:80/path", "http://a@127.0.0.1:80", "http://127.0.0.1:80?q=1"])
def test_no_public_network_or_redirect_targets(url):
    with pytest.raises(ValueError):
        local_url(url)


def test_http_rejections_timeout_and_recovery(tmp_path):
    h = Harness(tmp_path)
    try:
        h.start("b")
        p = h.packet("intent.publish.json", "a")
        status, reply = request(h.ports["b"], h.token, encode(p), auth=False)
        assert status == 401 and reply["error"]["code"] == "AUTH_REQUIRED"
        status, reply = request(h.ports["b"], h.token, b'{"x":1,"x":2}')
        assert status == 400 and reply["error"]["code"] == "INVALID_JSON"
        status, reply = request(h.ports["b"], h.token, b' ' * 65537)
        assert status == 413 and reply["error"]["code"] == "MESSAGE_TOO_LARGE"
        p["sender"]["participant_id"] = "spoofed-organization"
        status, reply = request(h.ports["b"], h.token, encode(p))
        assert reply["payload"]["reason_code"] == "SENDER_MISMATCH"
        with socket.create_connection(("127.0.0.1", h.ports["b"]), timeout=4) as conn:
            conn.sendall(f"POST {ENDPOINT} HTTP/1.1\r\nHost: 127.0.0.1\r\nAuthorization: Bearer {h.token}\r\nContent-Type: application/json\r\nContent-Length: 10\r\n\r\n{{".encode())
            chunks = []
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                chunks.append(data)
            response = b"".join(chunks)
            assert b"408" in response and b'"TIMEOUT"' in response
        p["sender"]["participant_id"] = h.ids["a"]
        assert request(h.ports["b"], h.token, encode(p))[1]["payload"]["status"] == "accepted"
        with sqlite3.connect(tmp_path / "b.sqlite3") as db:
            assert db.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 1
    finally:
        h.close()


def test_client_timeout_keeps_durable_outbox(tmp_path):
    # Synthetic fault injection: a real local socket accepts but never returns HTTP.
    h = Harness(tmp_path)
    ready = threading.Event()
    def slow_endpoint():
        with socket.socket() as server:
            server.bind(("127.0.0.1", h.ports["b"]))
            server.listen(1)
            server.settimeout(5)
            ready.set()
            conn, _ = server.accept()
            with conn:
                conn.recv(65536)
                time.sleep(.5)
    worker = threading.Thread(target=slow_endpoint)
    worker.start()
    assert ready.wait(2)
    p = h.packet("intent.publish.json", "a")
    path = tmp_path / "timeout.json"
    path.write_bytes(encode(p))
    result = h.cli("a", "send", "--peer", h.ids["b"], "--message", str(path), "--timeout", ".1")
    worker.join(timeout=3)
    assert result["status"] == "pending" and result["code"] == "TIMEOUT"
    with sqlite3.connect(tmp_path / "a.sqlite3") as db:
        row = db.execute("SELECT state,attempts,last_code FROM outbox").fetchone()
        assert row == ("pending", 1, "TIMEOUT")


@pytest.mark.parametrize("revocation,expected_code", [("recipient", "PRIVACY_DENIED"), ("peer", "UNKNOWN_PEER")])
def test_retry_rechecks_revoked_authority_before_network(tmp_path, monkeypatch, revocation, expected_code):
    h = Harness(tmp_path)
    packet = h.packet("intent.publish.json", "a")
    raw = encode(packet)
    peer = h.ids["b"]
    store = Store(tmp_path / "a.sqlite3", h.ids["a"])
    store.accept(raw, h.ids["a"], outgoing=True, peer=peer, selected=[peer])
    config = json.loads((tmp_path / "a.local.json").read_text())
    if revocation == "recipient":
        config["selected_recipients"] = []
    else:
        config["peers"] = {}
        config["selected_recipients"] = []
    def forbidden_network(*args, **kwargs):
        pytest.fail("No connection may be created after disclosure authority is revoked")
    monkeypatch.setattr("odip.node.http.client.HTTPConnection", forbidden_network)
    result = deliver(store, config, peer, store.pending()[0]["raw"])
    assert result["status"] == "blocked" and result["code"] == expected_code
    assert store.pending() == []
    with sqlite3.connect(tmp_path / "a.sqlite3") as db:
        assert db.execute("SELECT state,last_code FROM outbox").fetchone() == ("blocked", expected_code)
        assert db.execute("SELECT raw FROM messages").fetchone()[0] == raw


def test_retry_authority_check_does_not_reapply_withdrawn_intent(tmp_path):
    h = Harness(tmp_path)
    peer, principal = h.ids["b"], h.ids["a"]
    store = Store(tmp_path / "a.sqlite3", principal)
    original = encode(h.packet("intent.publish.json", "a"))
    store.accept(original, principal, outgoing=True, peer=peer, selected=[peer])
    withdrawn = encode(h.packet("intent.withdraw.json", "a"))
    store.accept(withdrawn, principal, outgoing=True, peer=peer, selected=[peer])
    assert store.authorize_outbound(original, peer, selected=[peer])["message_type"] == "intent.publish"
    with sqlite3.connect(tmp_path / "a.sqlite3") as db:
        assert db.execute("SELECT withdrawn FROM intents").fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 2


@pytest.mark.parametrize("case,http_status,expected_state,expected_code", [
    ("error-on-success", 200, "pending", "INVALID_RECEIPT"),
    ("error-list", 400, "pending", "INVALID_RECEIPT"),
    ("empty-error", 400, "pending", "INVALID_RECEIPT"),
    ("business-error-without-ack", 403, "pending", "INVALID_RECEIPT"),
    ("accepted-ack-on-error", 400, "pending", "INVALID_RECEIPT"),
    ("transport-unauthorized", 401, "rejected", "AUTH_REQUIRED"),
    ("business-rejected-ack", 400, "rejected", "UNKNOWN_INTENT"),
    ("rejected-ack-on-success", 200, "pending", "INVALID_RECEIPT"),
])
def test_untrusted_peer_responses_cannot_silently_stop_retries(tmp_path, monkeypatch, case, http_status, expected_state, expected_code):
    # Fault-injected HTTP replies; the real socket path is covered separately.
    h = Harness(tmp_path)
    peer, principal = h.ids["b"], h.ids["a"]
    store = Store(tmp_path / "a.sqlite3", principal)
    raw = encode(h.packet("intent.publish.json", "a"))
    packet_id = json.loads(raw)["message_id"]
    store.accept(raw, principal, outgoing=True, peer=peer, selected=[peer])
    config = json.loads((tmp_path / "a.local.json").read_text())
    response_packet = h.packet("receipt.ack.json", "b")
    response_packet["payload"] = {"original_message_id": packet_id, "status": "accepted"}
    if case in {"error-on-success", "transport-unauthorized"}:
        response_packet = {"error": {"code": "AUTH_REQUIRED", "reason": "Test authentication failed"}}
    elif case == "error-list":
        response_packet = {"error": []}
    elif case == "empty-error":
        response_packet = {"error": {}}
    elif case == "business-error-without-ack":
        response_packet = {"error": {"code": "FORBIDDEN", "reason": "Business refusal must be an ACK"}}
    elif case in {"business-rejected-ack", "rejected-ack-on-success"}:
        response_packet["payload"].update(status="rejected", reason_code="UNKNOWN_INTENT")
    response_raw = encode(response_packet)
    calls = []
    class Response:
        status = http_status
        def read(self, limit):
            return response_raw[:limit]
    class Connection:
        def __init__(self, *args, **kwargs):
            pass
        def request(self, *args, **kwargs):
            calls.append("request")
        def getresponse(self):
            return Response()
        def close(self):
            calls.append("close")
    monkeypatch.setattr("odip.node.http.client.HTTPConnection", Connection)
    result = deliver(store, config, peer, raw)
    assert result["status"] == expected_state and result["code"] == expected_code
    assert calls == ["request", "close"]
    with sqlite3.connect(tmp_path / "a.sqlite3") as db:
        assert db.execute("SELECT state,last_code FROM outbox").fetchone() == (expected_state, expected_code)
        # Invalid peer statements must not enter the trusted local message log.
        expected_messages = 2 if case == "business-rejected-ack" else 1
        assert db.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == expected_messages
