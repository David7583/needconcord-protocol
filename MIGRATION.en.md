# Versioning and migration

[简体中文](MIGRATION.md) | **English**

The public name is **NeedConcord Protocol**. Its historical working name was Open Demand Interoperability Protocol (ODIP). The public-name change affects documentation display and release-package naming only. The wire identifier remains `ODIP/0.1.3-exp.1`; Schema identifiers, message fields, test data and the `odip` Python module are not renamed. Implementations already using this wire version do not need to convert messages for the public-name change. Do not replace `ODIP` inside stored messages or change their original byte digests. Any future unification of machine identifiers will have its own version, migration steps and compatibility tests.

This release revises the `ODIP/0.1.2` draft. Its experimental wire identifier is `ODIP/0.1.3-exp.1`, and the Python project version is `0.1.3.dev1`. The maintainer retains the complete historical archive offline. The public package's `tests/fixtures/v0.1.2/` directory supplies the minimum old Schema and synthetic inputs required for migration.

The candidate tightens validation for some inputs accepted by the original Schema. **It is not a transparently compatible patch.** Experimental 0.x versions may introduce explicitly documented breaking validation changes. Old nodes must explicitly reject unsupported versions, and new nodes do not automatically accept the original version. There is no negotiation or field guessing. See the [protocol changes](docs/PROTOCOL-DELTA.en.md) for affected fields, semantics and impacts. Earlier IRP/ODIP versions preceding v0.1.2 are not automatically compatible either.

The conservative migration tool replaces the protocol identifier and writes a new file only when the old Schema check and the new stateless validation both pass:

```powershell
.\.venv\Scripts\python.exe scripts/migrate.py tests/fixtures/v0.1.2/examples/intent.publish.json .tmp/migrated-intent.json
```

The source file is never modified, and an existing destination is rejected. Missing relationship IDs, timestamps outside the candidate's UTC format, unknown evidence types, excessive revenue shares and similar cases require human review. The tool does not invent IDs, alter original wording, fabricate user confirmation or infer authorization. This conversion checks stateless validity only: it does not establish that the target node holds the related intent, that the publisher has permission or that the user actually authorized the action. The migrated message is an exchange under a new version and has a different byte digest; do not treat it as a retry of the original message.

Suggested upgrade process: archive the version and original bytes; run both versions' public validation offline; review rejected cases; explicitly enable the candidate version on both sides; replay reviewed lifecycles in a separate state space; retain failure and conversion records. Do not bulk-convert a production database in place.

The candidate retains the original example's meaning of `share_rate`: it uses the same calculation base as `fee_rate`, and the shares must not exceed the total fee rate. It does not mean a percentage of service-fee revenue. A different meaning needs a new extension or field rather than reuse of the existing field. This is disclosure, not fee collection. `consent_recorded=false` may disclose that consent has not been obtained, but must not trigger a charge. Changes to this interpretation or the state/permission policies may be proposed through a public RFC, with compatibility impacts explicitly documented.
