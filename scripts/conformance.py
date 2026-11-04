"""Implementation-neutral public conformance runner. No import of reference code."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from decimal import Decimal
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def dump_exact(value):
    """Generic JSON bridge preserving decimal values; contains no ODIP oracle."""
    if isinstance(value, Decimal):
        if not value.is_finite(): raise ValueError("non-finite JSON number")
        return str(value)
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + dump_exact(v) for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ",".join(map(dump_exact, value)) + "]"
    return json.dumps(value, ensure_ascii=False, allow_nan=False)

def run(command, report, profile="full"):
    manifest = json.loads((ROOT / "conformance/manifest.json").read_text(encoding="utf-8"))
    results, skipped = [], []
    for category in ("vectors", "sequences"):
        for item in manifest[category]:
            if profile == "core" and item.get("requires"):
                skipped.append({"id": item["id"], "requires": item["requires"]})
                continue
            data = json.loads((ROOT / "conformance" / item["file"]).read_text(encoding="utf-8"), parse_float=Decimal)
            if category == "vectors":
                request = {"operation": "validate", "packet": data}
                expected = {"code": item["expected_code"]}
            else:
                # Never send expected answers to the adapter.
                request = {"operation": "sequence", "steps": [{k: v for k, v in s.items() if not k.startswith("expected_")} for s in data["steps"]]}
                expected = {"results": [{"status": s["expected_status"], "code": s["expected_code"]} for s in data["steps"]]}
            try:
                p = subprocess.run(command, input=dump_exact(request)+"\n", capture_output=True,
                                   encoding="utf-8", timeout=20, cwd=ROOT)
                actual = json.loads(p.stdout) if p.returncode == 0 else {"adapter_exit": p.returncode}
                success = actual == expected
            except (subprocess.TimeoutExpired, ValueError, OSError) as exc:
                actual, success = {"adapter_error": type(exc).__name__}, False
            results.append({"id": item["id"], "passed": success, "expected": expected, "actual": actual})
    result = {"protocol": manifest["protocol"], "executed_at": datetime.now(timezone.utc).isoformat(),
              "adapter_command": command, "scope": "Public vectors and state sequences; does not certify network security or independent implementation",
              "profile": profile, "skipped": skipped, "total": len(results), "passed": sum(r["passed"] for r in results), "results": results}
    Path(report).parent.mkdir(parents=True, exist_ok=True)
    Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Conformance: {result['passed']}/{result['total']}; report: {report}")
    for row in results:
        if not row["passed"]:
            print(json.dumps(row, ensure_ascii=False))
    return int(result["passed"] != result["total"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="reports/conformance-run.json")
    parser.add_argument("--profile", choices=["core", "full"], default="full")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("provide adapter executable after --")
    sys.exit(run(command, args.report, args.profile))
