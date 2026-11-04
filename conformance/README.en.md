# NeedConcord Protocol public conformance assets

[简体中文](README.md) | **English**

This directory is for independent implementers. All test data is synthetic; identities, goods, quotations and confirmation statements do not represent participation by real organizations. The public name is NeedConcord Protocol and the wire identifier remains `ODIP/0.1.3-exp.1`. The prose contract is in [specification section 15](../SPEC-en.md); the structural contract is the [packet schema](../schemas/packet.schema.json). These are public conformance assets for an experimental version. See [provenance](../docs/PROVENANCE.en.md) for the scope of licensing rights. The English specification is a translation; the Chinese specification remains the normative prose.

Implementations need not use Python. The JSON test data and expected results do not import the reference implementation. In `manifest.json`:

- `vectors`: `id` is a stable case name; `file` is relative to this directory; `layer` is `schema` or `semantic`; `schema_valid` is the separate structural-layer expectation; `expected_code=null` means acceptance at the specified layer; `rule` identifies the specification rule; `requires` lists optional commerce/fulfillment support required by the case, with an empty array denoting core functionality.
- `sequences`: each case in a file starts from empty state and processes its `steps` in order. `packet` is the message and `principal` is the identity authenticated by the external test fixture. For each step, `expected_status` is `accepted`/`rejected`/`duplicate`, and `expected_code` is an error code or `null`. Authentication does not come from the message's self-declaration. A sequence's `requires` includes any optional capability needed by its steps; `core-lifecycle` does not require the fulfillment extension.
- Single-packet semantic cases do not require prior business history; sequences check previously published intents, permissions and revisions. This avoids treating `UNKNOWN_INTENT` as a structural-validation failure.

The asset set includes valid and invalid packets for each of the eight message types, missing associations, date formats, cross-field conflicts, unjustified inferred assertions, commerce-extension constraints, privacy scope, lifecycle behavior, duplicates and conflicts, authorization, withdrawal and unknown references. Further network-failure, restart and resource-limit checks run through the engineering-test entry point. A negative single-packet case contains only the error being tested; for packets with multiple errors, implementations are not required to select exactly the same first diagnostic.

## Adapter interface for external implementations

`scripts/conformance.py` invokes an external command as a JSONL adapter, which may be written in any language. Each input line contains one JSON object and each output line contains one JSON object. stdout must contain results only; diagnostics go to stderr. The runner must not import the reference protocol implementation to decide an external implementation's results.

Validation input: `{"operation":"validate","packet":{...}}`. Output: `{"code":null}`, `{"code":"ID_MISMATCH"}` or another applicable code. The adapter performs structural and single-packet protocol-semantic validation. The runner does not send manifest expectations or rule labels to the adapter. `schema_valid` is available for independent structural testing; the full conformance entry point compares results against `expected_code`.

Sequence input: `{"operation":"sequence","steps":[{"packet":{...},"principal":"..."}]}`. Output: `{"results":[{"status":"accepted","code":null},...]}`. Each sequence MUST create empty storage. The runner removes `expected_status`/`expected_code`; the adapter must not read the test directory and copy the answers. When a sequence repeatedly supplies the same packet, the adapter should reuse identical bytes after its first serialization of that packet. Byte differences on the actual network are tested separately.

Use `scripts/conformance.py --help` for the command interface. Implementers supply their adapter command and receive JSON results they can save. Passing through the reference adapter only shows consistency between the test entry point and the reference implementation. Independent implementations should publish their language, source revision, adapter, configuration and original output. Calling the reference library through the reference adapter must not be presented as cross-implementation interoperability.

The runner supports `--profile core` and `--profile full`, defaulting to `full`. The core profile skips packets and whole sequences marked as depending on optional capabilities; lacking an optional extension does not by itself mean core non-conformance. Reports must distinguish executed and skipped cases rather than count skips as passes. For example:

```powershell
.\.venv\Scripts\python.exe scripts\conformance.py --profile core --report reports\conformance-core.json -- .\.venv\Scripts\python.exe reference\conformance_adapter.py
.\.venv\Scripts\python.exe scripts\conformance.py --profile full --report reports\conformance-full.json -- .\.venv\Scripts\python.exe reference\conformance_adapter.py
```

The adapter, runner and message implementation must preserve JSON decimal precision. In the high-precision negative case `commerce-precision-overallocation`, the allocation sum `0.10000000000000000000000001 + 0.2` is strictly greater than `0.3` and must return `COMMERCE_INVALID`. Converting the numbers to binary floating point before reserialization changes the input, so it cannot establish a pass against the original vector. Exact decimals or preservation of original number tokens can be used; no particular language library is required.

## Coverage boundaries

Schema validation must enable Draft 2020-12 `uuid`/`date-time` format assertions. Loading a schema without enabling these assertions cannot be reported as a pass. Commerce is treated as a supported extension in the test suite and must therefore be validated; a core-only implementation should explicitly state that this optional extension is not covered. The tests do not verify real contracts, product quality, genuine user authorization, global naming uniqueness, payment security, full compliance with privacy laws or third-party certification.

Public tests use the plain JSON assets and manifest in this directory directly; no internal development generator or complete historical archive is required. Changes to test assets must provide their specification basis, expected behavior and compatibility analysis. Do not change expected results to match the behavior of a particular implementation.
