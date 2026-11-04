"""Conservative explicit 0.1.2 -> experimental conversion; never guess missing facts."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odip import PROTOCOL
from odip.validation import Rejection, decode, encode, validate

def migrate(packet):
    old = json.loads((ROOT/"tests/fixtures/v0.1.2/schemas/packet.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(old, format_checker=FormatChecker()).validate(packet)
    candidate = deepcopy(packet)
    candidate["protocol"] = PROTOCOL
    # Baseline timestamps, authority, privacy and IDs are never fabricated or silently normalized.
    validate(decode(encode(candidate)))
    return candidate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.source.resolve() == args.destination.resolve() or args.destination.exists():
        parser.error("destination must be a new file, distinct from source")
    try:
        candidate = migrate(decode(args.source.read_bytes()))
        output = encode(candidate) + b"\n"
    except Exception as exc:
        print(json.dumps({"migrated": False, "reason": getattr(exc, "code", type(exc).__name__), "action": "Manual review required; no output written"}))
        sys.exit(1)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    with args.destination.open("xb") as f:
        f.write(output)
    print(json.dumps({"migrated": True, "scope": "stateless only; recheck authority and relationship context before sending"}))
