# NeedConcord Protocol 0.1.3-exp.1 — Experimental Pre-release

[简体中文](RELEASE-NOTES-0.1.3-exp.1.md) | **English**

Positioning: Experimental Draft / Experimental Pre-release. This version is not a formal standard, industry certification or production commercial network.

The public name is **NeedConcord Protocol**. Its former working name was Open Demand Interoperability Protocol (ODIP). The machine protocol identifier remains **`ODIP/0.1.3-exp.1`**. The name change does not alter schema identifiers, message fields, test vectors, the `odip` module or existing protocol rules; stored messages need no conversion for this change. Any future change to the machine identifier must follow an explicit version migration.

Starting from the designated v0.1.2 archive, this work examined whether others can read the protocol, implement it independently and test it using public assets. Deliverables include the Chinese specification, schemas, positive and negative examples for every core message type, public semantic/state tests, an external-adapter interface and minimal reference nodes running in two processes.

`ODIP/0.1.3-exp.1` uses a distinct version identifier because it narrows the accepted input set and adds state, permission and idempotency conventions. Old packets are not automatically compatible; review them under [MIGRATION.en.md](../MIGRATION.en.md). This version introduces no protocol tax, central-service dependency, payment execution or permanent buyer/seller roles. A solution without a transaction may satisfy a need, and transaction confirmation does not automatically mean the need is resolved.

See [validation scope](VALIDATION.en.md) for what was actually verified; execution results are in `evidence/`. Two independent processes of the same Python implementation exchange data through real loopback sockets, persist independently and recover. There is no evidence of cross-language or cross-team implementation interoperability, and no public-network security validation. All examples and identities are synthetic.

The commerce extension is disclosure only. Its same-basis allocation constraint is an explicit interpretation in this candidate, not an entitlement to charge fees. Privacy declarations are not actual user authorization, and HTTP test tokens are not production identities. Storage retains history; deletion propagation and governance of real personal data are not implemented.

The GitHub community uses open, maintainer-led governance, with Chinese/English issue, PR and RFC templates and three substantive discussion topics. Core changes require public discussion, compatibility analysis, tests and maintainer review; voting does not amend the specification automatically. See [community guidance](COMMUNITY.md), [security reporting](../SECURITY.md) and the [code of conduct](../CODE_OF_CONDUCT.md) for categories and reporting channels. Feature availability depends on the repository's actual settings.

Licensing follows the scope of rights that can be granted: Apache-2.0 for code, schemas and tests, and CC BY 4.0 for original documentation. The Project Initiator and Initial Maintainer is publicly identified as David7583. Research, writing and verification used AI assistance; there is no guarantee of certain or exclusive ownership of all historical or third-party content. See [provenance](PROVENANCE.en.md), [NOTICE](../NOTICE.en.md) and the [dependency inventory](../LICENSES/dependency-licenses.json).

The source package contains only reviewed specifications, schemas, reference code, tests, examples, licenses, community materials and sanitized validation evidence. Per-file SHA-256 values are in `PUBLIC-MANIFEST.json`. The complete original draft, internal audits, personal environment records and local Git history are excluded.
