# Changelog

[简体中文](CHANGELOG.md) | **English**

## 0.1.3-exp.1 — 2026-11-04, Experimental Draft / Pre-release

- Adopted NeedConcord Protocol as the public name while retaining the `ODIP/0.1.3-exp.1` wire identifier and existing Schemas, message structures, test vectors and Python module. The name change introduces no additional wire-compatibility change.
- Continued development from the designated v0.1.2 draft. The complete original archive and audit evidence remain offline; the public package contains only the minimum necessary compatibility fixtures from the old version.
- Added deterministic rules by validation layer, positive and negative vectors for every message type, state sequences and an external conformance runner independent of the reference implementation.
- Clarified demand relationships, UTC/UUID formats, evidence limits, known extensions and commercial revenue sharing. A new wire identifier records incompatible validation tightening.
- Added two independent processes, separate SQLite storage, actual loopback HTTP, idempotency/conflict checks, an outbox and recovery after restart.
- Pinned the interpreter and dependency hashes and provided repeatable verification commands, actual failure records and final evidence.
- Provided Chinese/English GitHub community templates, open governance and three substantive discussion drafts. Feature availability depends on the repository's actual settings.
- Documented license scopes confirmed by the initiator while preserving historical provenance and AI-assisted rights limitations.

Missing date-format dependencies and initial execution problems were fixed; historical records remain offline. Evidence for the public candidate was generated separately; see [validation scope](docs/VALIDATION.en.md). Full protocol changes are described in [PROTOCOL-DELTA](docs/PROTOCOL-DELTA.en.md).

## 0.1.2 — designated historical baseline

The original version provided an initial draft, Schemas and an in-process demo for intents, capabilities, proposals, outcomes and receipts. This candidate does not represent that original demo as independent-process or cross-implementation validation. Original materials remain archived offline.
