# Provenance, modifications and copyright boundaries

[简体中文](PROVENANCE.md) | **English**

This record applies to the public source of **NeedConcord Protocol 0.1.3-exp.1**, whose wire identifier is `ODIP/0.1.3-exp.1`. **David7583** initiated the project, leads its design and serves as the initial maintainer. AI assisted research, drafting and validation. The public display name does not introduce an unconfirmed real name or institution.

The initiator's authorization covers only original or lawfully licensable material. AI assistance does not automatically establish copyrightability, complete originality, the absence of similar third-party expression or exclusive ownership. No unconditional guarantee is made on those points. Other authors, library authors and owners of license texts retain their respective rights.

## Sources of public materials

| Material | Observable source and changes | Rights boundary |
|---|---|---|
| `SPEC-zh-CN.md`, `BUSINESS-BOUNDARY.md`, version and migration notes | Continued revisions of the initiator-provided v0.1.2 draft, retaining its goals; new rules and differences are described in PROTOCOL-DELTA | Authorized specification prose uses CC BY 4.0; the historical creation chain lacks complete independent evidence, so complete originality is not claimed as proven |
| `schemas/` and material derived from the original seven `examples/` files | Revised from the same draft's Schemas and synthetic examples; Schemas include modification notices | Apache-2.0 within the authorized scope; examples are not actual users, goods, contracts or third-party integration data |
| `tests/fixtures/v0.1.2/` | Minimum old Schema and synthetic inputs retained for migration and compatibility, with per-file provenance alongside them | Authorization does not extend to unauthorized historical or third-party rights; the complete development archive is excluded |
| `odip/`, `reference/`, `scripts/`, added `tests/` and public vectors | AI-assisted reference code, automation and test assets written from the specification; two processes using the same library are not counted as independent implementations | Authorized code, tests and machine-readable assets use Apache-2.0 |
| README, contribution/governance/security documents, tutorials, community templates and discussion drafts | Written for this project's needs, without copying an entire third-party community code-of-conduct template; relevant sections identify sources for public facts and operating instructions | Original prose uses CC BY 4.0; code/configuration portions use Apache-2.0; third-party quotations remain attributable to their original sources |
| `LICENSE`, `LICENSES/CC-BY-4.0.txt` | Complete official Apache-2.0 and CC BY 4.0 license texts | Original texts are retained, not claimed as project-created works; no endorsement by Apache or Creative Commons is implied |
| `LICENSES/dependencies/` | Upstream license/copyright notices extracted from pinned dependency distributions | Each upstream license remains applicable; the project's license does not replace the licenses of those libraries |
| `evidence/` | Sanitized test output, counts and digests produced by actual execution against a public source snapshot | Execution facts, not proof of identity, provenance, actual transactions or third-party certification |

Dependency versions, SHA-256 values, upstream license fields and filenames appear in [LICENSES/dependency-licenses.json](../LICENSES/dependency-licenses.json). The source package includes no interpreter, virtual environment, downloaded wheels or actual business data. Future binary, container or vendored-library distributions require a fresh review of the components actually included and their complete notices; the current package-level review does not replace that work.

## Historical materials and uncertainty

The maintainer retains the complete v0.1.2 draft, original ZIP, internal environment details and historical test/audit records offline. They are not included in the public repository by default. Public change records and minimum migration fixtures preserve necessary traceability; public conformance tests do not require access to the maintainer's internal materials.

The original draft did not provide complete paragraph-by-paragraph creation records or a third-party source inventory. In the reviewed draft materials, apart from standard license texts and cited public facts, no code fragments with explicit third-party copyright headers were identified. **Not finding material does not prove it is absent.** Platform names in the original draft were examples, not evidence of integration, partnership or authorization. User-confirmation and transaction statements in historical examples are treated as synthetic data.

If material is later confirmed to originate from a third party, preserve the author, original license, source and modification notes. AI involvement is not a reason to remove attribution. If necessary permission cannot be obtained, stop distributing that portion, replace or remove it or obtain authorization, then rerun affected tests. Material with unverified provenance must not simply be labeled as David7583's original work.

The public name NeedConcord Protocol and the historical working name ODIP refer to the same project. Renaming does not change licenses or technical compatibility, and copyright licenses do not grant exclusive trademark rights. Change records do not establish automatic compatibility with old versions or other organizations. See [LICENSE-DOCS](../LICENSE-DOCS.en.md) and [NOTICE](../NOTICE.en.md) for the applicable scope.
