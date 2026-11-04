# NeedConcord Protocol (NCP)

[简体中文](README.md) | **English**

A demand-first, role-neutral open protocol for interoperable demand exchange. **Version `0.1.3-exp.1`, Experimental Draft / Experimental Pre-release.** The public name is **NeedConcord Protocol**; the validated machine-readable protocol identifier remains **`ODIP/0.1.3-exp.1`**.

**Validation status: Schema validation and local independent-process validation have passed. Production network security and cross-implementation interoperability remain unverified; no pass is claimed for either.** The experimental release has 91/91 engineering tests, 53/53 full-profile conformance cases and 42/42 core-profile conformance cases passing, with 11 optional cases explicitly skipped in the core profile. This evidence applies to the released `v0.1.3-exp.1` snapshot; see the [validation scope](docs/VALIDATION.en.md).

This project evolved from the Open Demand Interoperability Protocol (ODIP) draft. The public-name change affects presentation and documentation only: Schema identifiers, message fields, the `odip` Python module and commands remain unchanged. Technical references to ODIP still refer to this protocol. The name does not assert exclusive trademark rights or third-party endorsement. Any future change to the wire identifier will require explicit versioning and migration rules.

Project Initiator and Initial Maintainer: **David7583**. AI assisted research, drafting and validation. See [NOTICE](NOTICE.en.md) for the copyright boundaries; historical and third-party materials are not all represented as exclusively owned by the initiator.

The first-stage deliverable is an open protocol that others can read, follow, implement independently and check against public conformance tests. It exchanges intents, capabilities, proposals, outcomes and receipts. Goods, services, custom work and non-transactional solutions can all participate.

Expressing a need is not a purchase commitment. Demand fulfillment and transaction status are independent. The protocol is free to use and requires no central node, platform account, designated operator or mandatory protocol fee. Preserve the user's original wording and distinguish inferences, confirmations and verified facts. Optional commercial services may charge fees. This project is independent of CONTINUUM and of any specific demand-side product.

## Start with the specification

The [Chinese specification](SPEC-zh-CN.md) is the current normative prose and remains authoritative if translations differ. Its [English translation](SPEC-en.md) supports readers; this English README is a project overview and usage guide, not a separate normative specification.

- [Specification and deterministic rules in English](SPEC-en.md) and [machine-readable Schema](schemas/packet.schema.json)
- [Public conformance tests and external implementation interface](conformance/README.en.md): JSON vectors, state sequences and an implementation-independent runner
- [Version migration](MIGRATION.en.md), [protocol changes](docs/PROTOCOL-DELTA.en.md) and [changelog](CHANGELOG.en.md)
- [Commercial and protocol boundaries](BUSINESS-BOUNDARY.en.md), [roadmap](ROADMAP.en.md) and [experimental release notes](docs/RELEASE-NOTES-0.1.3-exp.1.en.md)
- [Reference nodes and running tutorial](docs/REFERENCE.en.md), plus [environment setup and reproduction](docs/ENVIRONMENT.en.md)
- [Security model and limitations](docs/SECURITY.en.md), and [validation scope and evidence](docs/VALIDATION.en.md)

## Local validation

On Windows x86_64 with CPython 3.12.7:

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/demo-01 --report evidence/two-process-evidence.json
```

The local demo starts two actual Python processes, uses separate SQLite files and transmits UTF-8 JSON over loopback HTTP. It exercises duplicate delivery, conflicts, retries after failure, lost receipts and recovery after restart. Example identities, goods and services are synthetic. Both processes use the same reference implementation, so this **does not establish cross-implementation, cross-organization or Internet security validation**. Adapters from other languages or teams can run the public tests without copying the reference implementation.

This candidate continues the initiator-provided v0.1.2 draft. The maintainer retains the complete original archive and internal audit records offline; they are not included in the public repository by default. The public source contains only the minimum old Schema and synthetic data needed for migration tests; see the [fixture provenance](tests/fixtures/v0.1.2/README.md). Third parties do not need the internal archive to run conformance tests. This experimental candidate rejects some inputs accepted by the original Schema and therefore uses a new wire identifier; interoperability with v0.1.2 is not automatically claimed.

## Contributing, governance and licensing

Contributions in Chinese or English are welcome. See the bilingual [contribution guide](CONTRIBUTING.md), [governance rules](GOVERNANCE.md), [code of conduct](CODE_OF_CONDUCT.md) and [security reporting policy](SECURITY.md). The bilingual [community guide](docs/COMMUNITY.md) describes GitHub discussion categories and three open questions; feature availability depends on the repository's actual settings. Core specification changes require public discussion, compatibility analysis, tests and maintainer review.

For material original to the initiator or which the initiator is legally entitled to license, code, Schemas, reference implementations and tests use [Apache-2.0](LICENSE), while original specification prose and technical documentation use [CC BY 4.0](LICENSE-DOCS.en.md). Third-party materials retain their original licenses. Full scope and the limits of AI-assisted provenance are documented in [NOTICE](NOTICE.en.md) and the [provenance record](docs/PROVENANCE.en.md). This is not an unconditional guarantee of copyright ownership for every item.
