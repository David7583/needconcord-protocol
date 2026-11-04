# Validation scope

[简体中文](VALIDATION.md) | **English**

Public name and version: **NeedConcord Protocol 0.1.3-exp.1** (Experimental Draft / Pre-release). Wire identifier: `ODIP/0.1.3-exp.1`. This directory and `evidence/` describe actual execution results for the reviewed public source tree; readers do not need the internal development archives. The public-name change did not alter schemas, message fields or conformance rules.

| Claim | Status |
|---|---|
| Schema validation passed | Supported by successful exit codes in this package's `evidence/verification-run.json` and the public test-vector results, covering all core types and the extensions declared as supported. |
| Local independent-process validation passed | Two actual server processes using the same Python implementation, separate SQLite databases and loopback HTTP. The two-process evidence records the original events. |
| Production network security validated | **Not verified.** No conclusion about public-network authentication, TLS or a production security audit. |
| Cross-implementation interoperability validated | **Not verified.** Two processes are not two independent implementations. |
| Other unverified areas | Real user authorization, external provenance and transaction facts, deletion propagation, sustained attack/capacity behavior and a complete supply-chain audit, among others. |

Public evidence:

- [Complete execution commands and exit codes](../evidence/verification-run.json)
- [Engineering-test JUnit report](../evidence/pytest.xml)
- [Full conformance profile](../evidence/conformance-run.json) and [core profile with explicit skips](../evidence/conformance-core-run.json)
- [Local two-process exchange, receipts, restart and recovery](../evidence/two-process-evidence.json)
- [Parent-process code coverage](../evidence/coverage.json)

Reports redact paths, machine identities and runtime test credentials while retaining case outcomes, error codes, timestamps and counts. All identities, intents, goods and transaction descriptions are synthetic. Receipts and the `user_confirmed` field are not proof of actual user consent. Parent-process coverage does not collect coverage from reference-node and adapter subprocesses and must not be interpreted as whole-system coverage.

On the supported Windows x86_64 / CPython 3.12.7 environment, install the hash-locked dependencies and run:

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
```

Public evidence covers the reviewed source snapshot. The public package contains a small attributed subset of v0.1.2 compatibility fixtures; it does not require private archives, the complete historical baseline or local Git history. See the [conformance contract](../conformance/README.en.md) for independent implementations and the [security model](SECURITY.en.md) for limitations.
