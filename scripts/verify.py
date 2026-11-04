"""Reproducible verification for a local archive or a self-contained public tree."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def synthetic_tokens():
    """Only inspect test-generated local configs; never export their contents."""
    found = set()
    for path in (ROOT/".tmp").rglob("*.local.json"):
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
            for peer in config.get("peers", {}).values():
                token = peer.get("token")
                if isinstance(token, str) and len(token) >= 32:
                    found.add(token)
        except (OSError, ValueError, AttributeError):
            continue
    return found


def sanitize(value, tokens=()):
    """Redact machine-specific paths and secrets without changing test outcomes."""
    if isinstance(value, dict):
        return {key: sanitize(item, tokens) for key, item in value.items() if key != "hostname"}
    if isinstance(value, list):
        return [sanitize(item, tokens) for item in value]
    if not isinstance(value, str):
        return value
    text = value
    for token in tokens:
        text = text.replace(token, "<redacted-test-token>")
    replacements = [(str(Path(sys.executable)), "python"), (str(ROOT), "."),
                    (str(Path(sys.base_prefix)), "<python-install>")]
    for original, replacement in replacements:
        for spelling in {original, original.replace("\\", "/")}:
            text = text.replace(spelling, replacement)
    text = re.sub(r"\b[A-Za-z]:[\\/][^\s\"<>]*", "<local-path>", text)
    text = re.sub(r"Bearer [A-Za-z0-9._~+/-]{24,}", "Bearer <redacted>", text)
    return text


def sanitize_reports(directory, tokens):
    for filename in ("coverage.json", "conformance-run.json", "conformance-core-run.json", "two-process-evidence.json"):
        path = directory/filename
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            path.write_text(json.dumps(sanitize(data, tokens), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    path = directory/"pytest.xml"
    if path.exists():
        junit = ET.parse(path)
        for element in junit.iter():
            element.attrib.pop("hostname", None)
            element.attrib.update({key: sanitize(value, tokens) for key, value in element.attrib.items()})
            if element.text:
                element.text = sanitize(element.text, tokens)
            if element.tail:
                element.tail = sanitize(element.tail, tokens)
        junit.write(path, encoding="utf-8", xml_declaration=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true", help="Verify without the private original ZIP/baseline")
    parser.add_argument("--report-dir", help="Relative output directory; defaults to evidence for public mode, or a new reports/release run directory")
    args = parser.parse_args(argv)
    os.chdir(ROOT)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    report_path = Path(args.report_dir or ("evidence" if args.public else f"reports/release/{run_id}"))
    if report_path.is_absolute() or not (ROOT/report_path).resolve().is_relative_to(ROOT):
        parser.error("--report-dir must be a relative directory within this checkout")
    report_dir = (ROOT/report_path).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    # Repeated public verification preserves preceding evidence instead of
    # silently replacing it. Publish only the reviewed current report set.
    previous = [report_dir/name for name in ("coverage.json", "conformance-run.json", "conformance-core-run.json", "two-process-evidence.json", "pytest.xml", "verification-run.json") if (report_dir/name).exists()]
    if previous:
        archive = report_dir/"history"/run_id
        archive.mkdir(parents=True, exist_ok=False)
        for path in previous:
            path.replace(archive/path.name)
    (ROOT/".tmp").mkdir(exist_ok=True)
    os.environ.update(TEMP=str(ROOT/".tmp"), TMP=str(ROOT/".tmp"), PYTHONIOENCODING="utf-8")
    py = sys.executable
    output = lambda name: (report_path/name).as_posix()
    commands = []
    if not args.public:
        commands.append([py, "scripts/verify_baseline.py"])
    commands.extend([
        [py, "-m", "pip", "check"],
        [py, "-m", "coverage", "run", "-m", "pytest", f"--basetemp=.tmp/pytest-{run_id}", "--junitxml="+output("pytest.xml")],
        [py, "-m", "coverage", "json", "-o", output("coverage.json")],
        [py, "-m", "coverage", "report"],
        [py, "scripts/conformance.py", "--report", output("conformance-run.json"), "--", py, "reference/conformance_adapter.py"],
        [py, "scripts/conformance.py", "--profile", "core", "--report", output("conformance-core-run.json"), "--", py, "reference/conformance_adapter.py"],
        [py, "reference/two_process_demo.py", "--work-dir", f".tmp/evidence-{run_id}", "--report", output("two-process-evidence.json")],
    ])
    runs = []
    for command in commands:
        print("RUN", " ".join(sanitize(command)), flush=True)
        try:
            process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
            stdout, stderr, code = process.stdout, process.stderr, process.returncode
        except subprocess.TimeoutExpired as exc:
            def as_text(data):
                return data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data or ""
            stdout, stderr, code = as_text(exc.stdout), as_text(exc.stderr)+"\nVerification command timed out", 124
        tokens = synthetic_tokens()
        print(sanitize(stdout, tokens), end="", flush=True)
        if stderr:
            print(sanitize(stderr, tokens), file=sys.stderr, flush=True)
        runs.append(sanitize({"command": command, "exit_code": code, "stdout": stdout, "stderr": stderr}, tokens))
        sanitize_reports(report_dir, tokens)
    result = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "mode": "public-source" if args.public else "local-research-archive",
        "environment": {"python": platform.python_version(), "platform": sys.platform, "architecture": platform.machine()},
        "runs": runs,
        "passed": all(item["exit_code"] == 0 for item in runs),
        "coverage_scope": "coverage.py parent-process Python lines/branches only; subprocess and network evidence reported separately",
        "redaction": "Executable/project/base-interpreter paths replaced by portable labels; JUnit hostname omitted; synthetic token values removed. Outcomes, timestamps and diagnostics retained.",
        "claim_limits": {"production_network_security_verified": False, "cross_implementation_interoperability_verified": False},
    }
    (report_dir/"verification-run.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Verification report:", output("verification-run.json"), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
