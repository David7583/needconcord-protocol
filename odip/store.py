"""Atomic persistence, owner authority and exact-byte replay protection."""
import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .validation import Rejection, decode, encode, validate_for_network


class Store:
    def __init__(self, path, participant_id):
        self.path = str(path)
        self.participant_id = participant_id
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY, digest TEXT NOT NULL,
                raw BLOB NOT NULL, direction TEXT NOT NULL, principal TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS intents(id TEXT PRIMARY KEY, owner TEXT NOT NULL,
                revision INTEGER NOT NULL, withdrawn INTEGER NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS proposals(id TEXT PRIMARY KEY, intent TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS outbox(id TEXT NOT NULL, peer TEXT NOT NULL,
                state TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
                last_code TEXT, PRIMARY KEY(id,peer));
            """)
            found = db.execute("SELECT value FROM metadata WHERE key='participant'").fetchone()
            if found and found[0] != participant_id:
                raise ValueError("Database belongs to another participant")
            db.execute("INSERT OR IGNORE INTO metadata VALUES('participant',?)", (participant_id,))

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA synchronous=FULL")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _privacy(self, packet, outgoing, peer, selected):
        kind = packet["message_type"]
        intent = packet["payload"] if kind == "intent.publish" else packet["payload"].get("intent") if kind == "intent.update" else None
        if intent:
            scope = intent["privacy"]["sharing_scope"]
            if scope == "private" or (outgoing and scope == "selected_participants" and peer not in selected):
                raise Rejection("PRIVACY_DENIED")

    def _outbound_privacy(self, db, packet, peer, selected):
        self._privacy(packet, True, peer, selected)
        if packet.get("intent_id"):
            prior = db.execute("SELECT payload FROM intents WHERE id=?", (packet["intent_id"],)).fetchone()
            if prior:
                scope = json.loads(prior["payload"])["privacy"]["sharing_scope"]
                if scope == "private" or (scope == "selected_participants" and peer not in selected):
                    raise Rejection("PRIVACY_DENIED")

    def authorize_outbound(self, raw, peer, *, selected=()):
        """Recheck current disclosure authority without reapplying historical state.

        Retries of already accepted messages remain possible after withdrawal,
        but withdrawing a recipient's grant blocks even an old queued message.
        """
        packet = validate_for_network(decode(raw))
        if packet["sender"]["participant_id"] != self.participant_id:
            raise Rejection("SENDER_MISMATCH")
        with self.connection() as db:
            self._outbound_privacy(db, packet, peer, selected)
        return packet

    def _apply(self, db, packet, principal):
        kind, p = packet["message_type"], packet["payload"]
        intent_id = packet.get("intent_id")
        if kind == "intent.publish":
            if db.execute("SELECT 1 FROM intents WHERE id=?", (intent_id,)).fetchone():
                raise Rejection("INTENT_EXISTS")
            db.execute("INSERT INTO intents VALUES(?,?,1,0,?)", (intent_id, principal, encode(p).decode("utf-8")))
        elif kind in {"intent.update", "intent.withdraw", "proposal.submit", "outcome.report", "fulfillment.quote"}:
            intent = db.execute("SELECT * FROM intents WHERE id=?", (intent_id,)).fetchone()
            if not intent:
                raise Rejection("UNKNOWN_INTENT")
            if kind in {"intent.update", "intent.withdraw", "outcome.report"} and intent["owner"] != principal:
                raise Rejection("FORBIDDEN")
            if intent["withdrawn"]:
                raise Rejection("INTENT_WITHDRAWN")
            if kind == "intent.update":
                if p["revision"] != intent["revision"] + 1:
                    raise Rejection("REVISION_CONFLICT")
                db.execute("UPDATE intents SET revision=?, payload=? WHERE id=?", (int(p["revision"]), encode(p["intent"]).decode("utf-8"), intent_id))
            elif kind == "intent.withdraw":
                db.execute("UPDATE intents SET withdrawn=1 WHERE id=?", (intent_id,))
            elif kind == "proposal.submit":
                if db.execute("SELECT 1 FROM proposals WHERE id=?", (p["proposal_id"],)).fetchone():
                    raise Rejection("PROPOSAL_EXISTS")
                db.execute("INSERT INTO proposals VALUES(?,?)", (p["proposal_id"], intent_id))
            elif kind == "fulfillment.quote":
                proposal = db.execute("SELECT intent FROM proposals WHERE id=?", (p["proposal_id"],)).fetchone()
                if not proposal:
                    raise Rejection("UNKNOWN_PROPOSAL")
                if proposal["intent"] != intent_id:
                    raise Rejection("ID_MISMATCH")
        elif kind == "receipt.ack":
            original = db.execute("SELECT 1 FROM outbox WHERE id=? AND peer=?", (p["original_message_id"], principal)).fetchone()
            if not original:
                raise Rejection("UNKNOWN_MESSAGE")

    def accept(self, raw, principal, *, outgoing=False, peer=None, selected=()):
        packet = validate_for_network(decode(raw))
        if packet["sender"]["participant_id"] != principal:
            raise Rejection("SENDER_MISMATCH")
        self._privacy(packet, outgoing, peer, selected)
        digest = hashlib.sha256(raw).hexdigest()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            if outgoing:
                self._outbound_privacy(db, packet, peer, selected)
            existing = db.execute("SELECT digest,principal FROM messages WHERE id=?", (packet["message_id"],)).fetchone()
            if existing:
                if existing["digest"] != digest or existing["principal"] != principal:
                    raise Rejection("ID_CONFLICT")
                status = "duplicate"
            else:
                self._apply(db, packet, principal)
                db.execute("INSERT INTO messages VALUES(?,?,?,?,?)", (packet["message_id"], digest, raw, "out" if outgoing else "in", principal))
                status = "accepted"
            if outgoing:
                db.execute("INSERT OR IGNORE INTO outbox(id,peer,state) VALUES(?,?,'pending')", (packet["message_id"], peer))
        return status, packet

    def pending(self):
        with self.connection() as db:
            return [dict(r) for r in db.execute("SELECT o.*,m.raw FROM outbox o JOIN messages m ON m.id=o.id WHERE state='pending' ORDER BY o.rowid")]

    def delivery(self, message_id, peer, state, code):
        with self.connection() as db:
            db.execute("UPDATE outbox SET state=?,attempts=attempts+1,last_code=? WHERE id=? AND peer=?", (state, code, message_id, peer))

    def export(self):
        with self.connection() as db:
            return [{"direction": r["direction"], "sha256": r["digest"], "packet": decode(r["raw"])} for r in db.execute("SELECT * FROM messages ORDER BY rowid")]
