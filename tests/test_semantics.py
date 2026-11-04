import copy
import json
from pathlib import Path
import uuid

import pytest

from odip.store import Store
from odip.validation import Rejection, decode, encode, validate_for_network

ROOT = Path(__file__).resolve().parents[1]


def sample(name):
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("raw,code", [(b'{"a":1,"a":2}', "INVALID_JSON"), (b'NaN', "INVALID_JSON"), (b'1e999999999', "INVALID_JSON"), (b'"\\ud800"', "INVALID_JSON"), (b'\xff', "INVALID_JSON"), (b'[' * 33 + b'0' + b']' * 33, "DEPTH_LIMIT"), (b' ' * 65537, "MESSAGE_TOO_LARGE")], ids=["duplicate-key", "nan", "exponent-limit", "surrogate", "bad-utf8", "depth", "oversize"])
def test_untrusted_json(raw, code):
    with pytest.raises(Rejection) as exc:
        decode(raw)
    assert exc.value.code == code

def test_exponent_beyond_decimal_parser_range_is_structured_rejection():
    with pytest.raises(Rejection, match="INVALID_JSON"):
        decode(b'{"x":1e999999999999999999999999999999999999999999}')


def test_atomic_rejection_and_restart(tmp_path):
    p = sample("intent.publish.json")
    store = Store(tmp_path / "test.sqlite3", "receiver")
    owner = p["sender"]["participant_id"]
    assert store.accept(encode(p), owner)[0] == "accepted"
    bad = sample("intent.update.json")
    bad["payload"]["revision"] = 4
    with pytest.raises(Rejection, match="REVISION_CONFLICT"):
        store.accept(encode(bad), owner)
    assert len(store.export()) == 1
    reopened = Store(tmp_path / "test.sqlite3", "receiver")
    assert reopened.accept(encode(p), owner)[0] == "duplicate"
    with pytest.raises(Rejection, match="ID_CONFLICT"):
        reopened.accept(json.dumps(p, indent=2, ensure_ascii=False).encode(), owner)
    with pytest.raises(ValueError, match="another participant"):
        Store(tmp_path / "test.sqlite3", "wrong-owner")


def test_selected_participants_is_explicit_and_private_never_sent(tmp_path):
    p = sample("intent.publish.json")
    owner = p["sender"]["participant_id"]
    store = Store(tmp_path / "test.sqlite3", owner)
    with pytest.raises(Rejection, match="PRIVACY_DENIED"):
        store.accept(encode(p), owner, outgoing=True, peer="b", selected=[])
    assert not store.export()
    assert store.accept(encode(p), owner, outgoing=True, peer="b", selected=["b"])[0] == "accepted"
    outcome = sample("outcome.no_purchase.json")
    with pytest.raises(Rejection, match="PRIVACY_DENIED"):
        store.accept(encode(outcome), owner, outgoing=True, peer="unselected", selected=["b"])
    p["payload"]["privacy"]["sharing_scope"] = "private"
    with pytest.raises(Rejection, match="PRIVACY_DENIED"):
        validate_for_network(p)


def test_no_state_change_on_inferred_claim_and_unknown_receipt(tmp_path):
    store = Store(tmp_path / "state.sqlite3", "receiver")
    p = sample("intent.publish.json")
    owner = p["sender"]["participant_id"]
    store.accept(encode(p), owner)
    outcome = sample("outcome.no_purchase.json")
    outcome["payload"]["evidence_source"] = "inferred"
    with pytest.raises(Rejection, match="INFERRED_ASSERTION"):
        store.accept(encode(outcome), owner)
    ack = sample("receipt.ack.json")
    with pytest.raises(Rejection, match="UNKNOWN_MESSAGE"):
        store.accept(encode(ack), ack["sender"]["participant_id"])
    assert len(store.export()) == 1


def test_original_text_and_unknown_extensions_preserved(tmp_path):
    p = sample("intent.publish.json")
    p["extensions"] = {"example.unrecognized": {"original_text": "Do not replace original"}}
    store = Store(tmp_path / "state.sqlite3", "receiver")
    store.accept(encode(p), p["sender"]["participant_id"])
    assert store.export()[0]["packet"] == p
    assert decode(encode(p)) == p


def test_exact_decimal_split_never_rounds_into_acceptance():
    p = sample("intent.publish.json")
    commerce = sample("commerce.example.json")
    commerce["fee_rate"] = 0.3
    commerce["payout_splits"][0]["share_rate"] = 0.1
    commerce["payout_splits"][1]["share_rate"] = 0.2
    p["extensions"] = {"commerce": commerce}
    raw = encode(p).replace(b'"share_rate":0.1', b'"share_rate":0.10000000000000000000000000000000000000000001')
    with pytest.raises(Rejection, match="COMMERCE_INVALID"):
        validate_for_network(decode(raw))
    precise = decode(b'{"n":0.10000000000000001,"small":1e-100}')
    assert decode(encode(precise)) == precise
