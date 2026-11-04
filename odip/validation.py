"""Public schema plus explicit semantic assertions. Local schemas only."""
import json
import math
from decimal import Decimal, InvalidOperation, localcontext
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.validators import extend
from . import PROTOCOL

MAX_BYTES = 65536
MAX_DEPTH = 32
ROOT = Path(__file__).resolve().parents[1]


class Rejection(Exception):
    def __init__(self, code, reason=None):
        self.code = code
        self.reason = reason or code
        super().__init__(self.reason)


def encode(packet):
    def render(value):
        if isinstance(value, Decimal):
            if not value.is_finite():
                raise ValueError("Non-finite number")
            return str(value)
        if isinstance(value, dict):
            return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + render(v) for k, v in value.items()) + "}"
        if isinstance(value, list):
            return "[" + ",".join(render(v) for v in value) + "]"
        return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    return render(packet).encode("utf-8")


def decode(raw):
    if len(raw) > MAX_BYTES:
        raise Rejection("MESSAGE_TOO_LARGE")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Rejection("INVALID_JSON", "Duplicate object key")
            result[key] = value
        return result
    def constant(_):
        raise Rejection("INVALID_JSON", "Non-finite number")
    def decimal_number(text):
        value = Decimal(text)
        if abs(value.as_tuple().exponent) > 10000:
            raise Rejection("INVALID_JSON", "Numeric exponent exceeds local resource limit")
        return value
    try:
        packet = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant, parse_float=decimal_number)
    except (ValueError, UnicodeError, RecursionError, InvalidOperation) as exc:
        raise Rejection("INVALID_JSON") from exc
    def inspect(value, depth=1):
        if depth > MAX_DEPTH:
            raise Rejection("DEPTH_LIMIT")
        if isinstance(value, str):
            try:
                value.encode("utf-8")
            except UnicodeError as exc:
                raise Rejection("INVALID_JSON") from exc
        if isinstance(value, float) and not math.isfinite(value):
            raise Rejection("INVALID_JSON")
        if isinstance(value, dict):
            for key, child in value.items():
                inspect(key, depth)
                inspect(child, depth + 1)
        elif isinstance(value, list):
            for child in value:
                inspect(child, depth + 1)
    inspect(packet)
    return packet


def validate_for_network(packet):
    """Stateless network admission; local private data is not a network packet."""
    validate(packet)
    kind = packet["message_type"]
    intent = packet["payload"] if kind == "intent.publish" else packet["payload"].get("intent") if kind == "intent.update" else None
    if intent and intent["privacy"]["sharing_scope"] == "private":
        raise Rejection("PRIVACY_DENIED")
    return packet


@lru_cache(maxsize=1)
def validator():
    if FormatChecker().conforms("2026-02-30T00:00:00Z", "date-time"):
        raise RuntimeError("date-time validation dependency missing; refusing fail-open startup")
    schema = json.loads((ROOT / "schemas/packet.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    types = Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda checker, value: not isinstance(value, bool) and isinstance(value, (int, float, Decimal)) and value == int(value))
    return extend(Draft202012Validator, type_checker=types)(schema, format_checker=FormatChecker())


def validate(packet):
    if isinstance(packet, dict) and packet.get("protocol") != PROTOCOL:
        raise Rejection("VERSION_UNSUPPORTED")
    if next(validator().iter_errors(packet), None) is not None:
        raise Rejection("SCHEMA_INVALID")
    p = packet["payload"]
    if "target_intent_id" in p and packet.get("intent_id") != p["target_intent_id"]:
        raise Rejection("ID_MISMATCH")
    if packet["message_type"] == "outcome.report":
        if p["evidence_source"] == "inferred" and (p["transaction_status"] == "confirmed" or p["need_status"] in {"satisfied", "partially_satisfied"}):
            raise Rejection("INFERRED_ASSERTION")
        if p["transaction_status"] == "confirmed" and not p.get("evidence_note", "").strip():
            raise Rejection("EVIDENCE_REQUIRED")
    commerce = packet.get("extensions", {}).get("commerce")
    if commerce is not None:
        splits = commerce.get("payout_splits", [])
        with localcontext() as context:
            # At most MAX_BYTES digits plus bounded exponent gap; no rounding.
            context.prec = MAX_BYTES + 20010
            total = sum((Decimal(str(s["share_rate"])) for s in splits), Decimal(0))
        if total > Decimal(str(commerce["fee_rate"])) or len({s["beneficiary"] for s in splits}) != len(splits):
            raise Rejection("COMMERCE_INVALID")
    return packet
