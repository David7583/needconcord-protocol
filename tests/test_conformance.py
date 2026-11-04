import json
import hashlib
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from odip.validation import Rejection
from odip.validation import decode
from scripts.migrate import migrate

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT/"conformance/manifest.json").read_text(encoding="utf-8"))

@pytest.mark.parametrize("item", MANIFEST["vectors"], ids=lambda x: x["id"])
def test_public_schema_expectations(item):
    schema = json.loads((ROOT/"schemas/packet.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    packet = json.loads((ROOT/"conformance"/item["file"]).read_text(encoding="utf-8"))
    assert validator.is_valid(packet) is item["schema_valid"]

def original(name):
    return json.loads((ROOT/"tests/fixtures/v0.1.2/examples"/name).read_text(encoding="utf-8"))

def test_migration_preserves_source_and_user_text():
    packet = original("intent.publish.json")
    before = deepcopy(packet)
    candidate = migrate(packet)
    assert packet == before
    assert candidate["protocol"] == "ODIP/0.1.3-exp.1"
    candidate["protocol"] = "ODIP/0.1.2"
    assert candidate == packet

@pytest.mark.parametrize("mutation", ["no_id", "offset_time", "inferred", "unvalidated_commerce"])
def test_migration_refuses_ambiguous_or_tightened_inputs(mutation):
    packet = original("outcome.no_purchase.json" if mutation == "inferred" else "intent.publish.json")
    if mutation == "no_id": del packet["intent_id"]
    if mutation == "offset_time": packet["timestamp"] = "2026-11-03T16:11:00+08:00"
    if mutation == "inferred": packet["payload"]["evidence_source"] = "inferred"
    if mutation == "unvalidated_commerce": packet["extensions"] = {"commerce": {"fee_rate": -1}}
    with pytest.raises(Rejection): migrate(packet)

def test_protocol_versions_are_not_silently_compatible():
    old_schema = json.loads((ROOT/"tests/fixtures/v0.1.2/schemas/packet.schema.json").read_text(encoding="utf-8"))
    new_schema = json.loads((ROOT/"schemas/packet.schema.json").read_text(encoding="utf-8"))
    old = original("intent.publish.json")
    new = migrate(old)
    assert not Draft202012Validator(new_schema).is_valid(old)
    assert not Draft202012Validator(old_schema).is_valid(new)

def test_every_message_type_has_positive_and_negative_public_vectors():
    types = {"intent.publish", "intent.update", "intent.withdraw", "capability.advertise", "proposal.submit", "outcome.report", "receipt.ack", "fulfillment.quote"}
    positive, negative = set(), set()
    for row in MANIFEST["vectors"]:
        packet = json.loads((ROOT/"conformance"/row["file"]).read_text(encoding="utf-8"))
        (positive if row["schema_valid"] else negative).add(packet["message_type"])
    assert types <= positive
    assert types <= negative

def test_migration_cli_preserves_decimal_amounts_and_refuses_overwrite(tmp_path):
    from decimal import Decimal
    packet = original("intent.publish.json")
    packet["payload"]["constraints"]["budget_ceiling"]["amount"] = 120.5
    packet["extensions"] = {"commerce": original("commerce.example.json")}
    source, destination = tmp_path/"source.json", tmp_path/"converted.json"
    source.write_text(json.dumps(packet, ensure_ascii=False), encoding="utf-8")
    original_bytes = source.read_bytes()
    command = [sys.executable, str(ROOT/"scripts/migrate.py"), str(source), str(destination)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    converted = decode(destination.read_bytes())
    assert converted["payload"]["constraints"]["budget_ceiling"]["amount"] == Decimal("120.5")
    assert converted["extensions"]["commerce"]["fee_rate"] == Decimal("0.0035")
    assert source.read_bytes() == original_bytes
    saved = destination.read_bytes()
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert destination.read_bytes() == saved

def test_public_compatibility_fixtures_match_recorded_sources():
    directory = ROOT/"tests/fixtures/v0.1.2"
    inventory = json.loads((directory/"manifest.json").read_text(encoding="utf-8"))
    assert len(inventory["files"]) == 4
    for row in inventory["files"]:
        assert hashlib.sha256((directory/row["path"]).read_bytes()).hexdigest() == row["sha256"]

def test_public_evidence_redacts_paths_and_tokens_without_changing_results():
    from scripts.verify import sanitize
    token = "synthetic" * 8
    diagnostic = str(ROOT/".tmp"/"case.json") + " " + str(Path(sys.executable)) + " Bearer " + token
    result = sanitize({"passed": False, "exit_code": 1, "hostname": "synthetic-host", "diagnostic": diagnostic}, {token})
    assert result["passed"] is False and result["exit_code"] == 1
    assert "hostname" not in result
    assert str(ROOT) not in result["diagnostic"]
    assert str(Path(sys.executable)) not in result["diagnostic"]
    assert token not in result["diagnostic"]
