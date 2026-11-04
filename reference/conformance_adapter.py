"""JSONL bridge for the Python reference; not an independent implementation."""
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from odip.validation import Rejection, decode, encode, validate_for_network
from odip.store import Store

def respond(request):
    if request["operation"] == "validate":
        try:
            validate_for_network(decode(encode(request["packet"])))
            return {"code": None}
        except Rejection as exc:
            return {"code": exc.code}
    if request["operation"] == "sequence":
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp)/"adapter.sqlite", "vector-test-receiver")
            results = []
            for step in request["steps"]:
                try:
                    status, _ = store.accept(encode(step["packet"]), step["principal"])
                    results.append({"status": status, "code": None})
                except Rejection as exc:
                    results.append({"status": "rejected", "code": exc.code})
            return {"results": results}
    raise ValueError("Unknown operation")

if __name__ == "__main__":
    for line in sys.stdin:
        print(json.dumps(respond(decode(line.encode("utf-8"))), ensure_ascii=False))
