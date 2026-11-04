# Environment and reproduction

[简体中文](ENVIRONMENT.md) | **English**

The public reference project fixes the environment to **CPython 3.12.7 on Windows x86_64**, with dependencies isolated in the repository's `.venv`. It does not require a particular distributor, global packages, workbench or commercial platform. Operators supply this interpreter version themselves; initialization does not change the global PATH, system Python or other projects' environments.

`.python-version` declares the interpreter version. `requirements.lock` pins dependencies and wheel SHA-256 values, including test tools. This lock covers Windows CPython 3.12 x86_64; it is not a claim of reproducibility across operating systems. Other platforms require separate lock-file review and execution of the same public tests. Dependency notices are in the [license inventory](../LICENSES/dependency-licenses.json). Pinning versions is not equivalent to completing a vulnerability audit.

Run from the root of the extracted or checked-out repository:

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
```

`python` must resolve to CPython 3.12.7. Alternatively, pass the path of an interpreter you have installed to `-Python`. Initialization checks the version, creates or reuses `.venv`, and installs dependencies against the hash lock. Activating the virtual environment is unnecessary. Package installation requires access to the package index. Handle execution-policy or network restrictions under your organization's rules; do not bypass them.

Public mode neither reads nor validates the maintainer's original ZIP, complete baseline or internal reports. The minimum materials required by compatibility tests are provided in [tests/fixtures/v0.1.2](../tests/fixtures/v0.1.2/README.md). The project source and public test assets are sufficient to run this phase of validation.

Individual commands:

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp=.tmp/pytest-public
.\.venv\Scripts\python.exe scripts/conformance.py --report evidence/conformance-run.json -- .\.venv\Scripts\python.exe reference/conformance_adapter.py
.\.venv\Scripts\python.exe scripts/conformance.py --profile core --report evidence/conformance-core-run.json -- .\.venv\Scripts\python.exe reference/conformance_adapter.py
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/manual-demo-01 --report evidence/two-process-evidence.json
```

Use a new, empty working directory for each two-node demonstration. `.tmp` and `runtime` may contain temporary test credentials, SQLite databases and full synthetic inputs; do not upload them with the source. Public reports contain only sanitized commands, synthetic data and structured events. The runner does not present expected results as actual passes. If the local system prohibits loopback communication, network tests will fail; rerun after obtaining legitimate execution permission, and never skip them and report a pass.

`rfc3339-validator` is a locked dependency required for date-format assertions. At startup, the service checks that invalid dates are actually rejected; it refuses to silently accept them when the dependency is absent. See [validation scope](VALIDATION.en.md) for public results and coverage definitions.

Configuration tokens bind test identities only; they do not authenticate real organizations. See [reference nodes](REFERENCE.en.md) for manual startup, retry and export instructions.
