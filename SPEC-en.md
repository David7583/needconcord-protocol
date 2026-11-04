# NeedConcord Protocol 0.1.3-exp.1 — Open demand interoperability protocol

[简体中文](SPEC-zh-CN.md) | **English**

This is a complete English translation for implementers. The [Chinese specification](SPEC-zh-CN.md) remains the current normative prose; this translation does not introduce a separate protocol version or new rules. Report discrepancies between the translations rather than silently changing an implementation's interpretation.

**Public name:** NeedConcord Protocol (NCP)  
**Former working name:** Open Demand Interoperability Protocol (ODIP)  
**Status:** Experimental Draft; not a formal industry standard  
**Document revision date:** 2026-11-04  
**Version:** `0.1.3-exp.1`  
**Protocol identifier:** `ODIP/0.1.3-exp.1`  
**Naming and compatibility:** ODIP remains the technical shorthand in the body of this document and refers to the same protocol as the public name NeedConcord Protocol. This public-name change does not alter the wire identifier, schemas, message structures or normative rules. The historical ODIP acronym has other uses; this project claims no exclusive naming rights.

**Revision provenance:** Revised from the v0.1.2 draft designated by the initiator; complete original archives are retained offline. See the [protocol revision table](docs/PROTOCOL-DELTA.en.md). The initiator has authorized Apache-2.0 for code, schemas and tests, and CC BY 4.0 for original documentation, to the extent that they have the right to license the material. This does not establish ownership of all material; see the [provenance record](docs/PROVENANCE.en.md) for the limits of verification of AI-assisted drafts and third-party sources. Section 15 defines deterministic rules that can be implemented independently; it does not establish verification by third-party implementations or production-network certification.

## 0. Definition in one sentence

ODIP provides an **open, portable and verifiable machine-to-machine representation** of needs, capabilities, proposals and need outcomes, without requiring a designated platform, payment provider or central server. It helps different participants express the problems they want to solve and the capabilities they can offer, and collaborate freely around specific needs. **The protocol itself is not a marketplace, payment system or financing product, and does not guarantee that a buyer and seller will complete a transaction.**

## 1. Design principles (normative)

1. **Demand first:** Center the problem to be solved, without assuming that a new product must be purchased. A response may offer goods, services, repairs, shared resources, a custom solution or an explicit inability to solve the problem.
2. **Role neutrality:** There are no permanent buyer, seller or logistics-provider identities. The same node may express needs and offer capabilities for different requests.
3. **Expression is not commitment:** Publishing an intent, responding with a proposal or viewing a quote must not be interpreted as a binding purchase commitment. Contracts and payments require separate, explicit authorization.
4. **Interoperability without lock-in:** Basic demand exchange must not depend on a designated operator, platform account, payment account, blockchain or private API. Nodes can export authorized data and migrate.
5. **Optional commerce and transparent fees:** The base ODIP protocol imposes no protocol tax. Operators may charge for services voluntarily purchased. Fee rates are not core protocol constants.
6. **No duplicate matching fees for the same billing unit:** The same transaction must not incur repeated fees on its full value merely because there are more nodes, supply-chain stages or participants. Independent services require separate disclosure of price, billing basis and authorization.
7. **Trust, not an oracle:** Distinguish the user's original words, AI inferences, user confirmations, external information and verified facts. Do not automatically count clicks or expressions of intent as completed transactions.
8. **Privacy minimization:** Do not disclose personally identifiable information by default. Explain collection, sharing, aggregation and commercial-analysis purposes separately and obtain appropriate authorization. Implementers must specify withdrawal rights and data-retention rules.
9. **Checkable fairness:** The protocol supports disclosure of paid promotion, ranking factors and data coverage. Whether discriminatory pricing or bias actually exists must be assessed through implementations, external audits and monitoring; the protocol cannot guarantee absolute fairness.
10. **Compatibility with existing markets:** E-commerce platforms, factories, logistics, inspection and financial providers, and independent Agents may participate through voluntary integration or lawfully authorized adapters. The protocol does not require bypassing any platform.

This document uses **MUST / SHOULD / MAY** to indicate levels of obligation. Real-world transaction obligations not covered here remain subject to contracts and applicable law.

## 2. Core objects and messages

**Participant:** May be a natural person's representative, a business, an Agent or an organizational node. One participant can have several `capabilities` (`express_demand` / `provide_goods` / `provide_services` / `provide_transport` / `provide_analysis`). A node's capability declaration is not proof of qualification.

**Intent:** Describes a real objective, constraints, acceptable alternatives and purchase readiness. The original text must be preserved. An interpretation extracted by AI should state whether the user has confirmed it.

**Proposal:** Returns candidate products or services, a custom solution, a non-transactional solution or no matching result for an intent. It may include total-cost components, matching gaps and evidence sources.

**Outcome:** Separately describes the degree to which the need was resolved and the transaction status. Completion of a transaction must not be used to infer that the need has been satisfied.

**Capability advertisement:** A voluntary declaration of resources and constraints a participant can offer; callers verify it independently.

**Fulfillment:** An optional, independent description of transport capacity, routes, timing, prices, loading/unloading, insurance and related matters. It may be another independent need or a sub-capability of the same purchasing proposal.

### 2.1 Core message types

| `message_type` | Purpose | Core required content |
|---|---|---|
| `intent.publish` | Publish a need | Original words, objective, readiness and acceptance of alternatives |
| `intent.update` | Modify a need | ID of the intent being modified and the updated intent |
| `intent.withdraw` | Withdraw a need | ID being withdrawn; optional withdrawal reason |
| `capability.advertise` | Declare a node's available capabilities | Supply type and description |
| `proposal.submit` | Offer a proposal or no result for a specific need | Target intent ID, proposal kind, description, information source and promotion disclosure; gaps are optional |
| `outcome.report` | Report whether the need was resolved and whether a transaction occurred | Target intent ID, two independent statuses and evidence source |
| `receipt.ack` | Acknowledge receipt or rejection of a message | Original message ID and processing status |

**Extension message (not required of core implementations):** `fulfillment.quote` (transport/fulfillment quotation). Core messages can still interoperate when this extension is absent.

### 2.2 Basic message envelope

Core packets share the following envelope:

- `protocol`: fixed to `ODIP/0.1.3-exp.1`;
- `message_id`: a unique UUID-format message ID; repeated delivery of the same ID and content should be handled idempotently;
- `message_type`: the message type;
- `timestamp`: a string in the UTC RFC 3339 subset defined in section 15;
- `sender`: `participant_id` (not proof of identity);
- `intent_id`: the correlation identifier for the same need; it may be omitted for messages unrelated to a need;
- `payload`: content validated according to the message type;
- `extensions`: optional extensions; unrecognized extensions must not change the meaning of core fields.

Production deployments MUST use authentication and authorization; they must not trust a node solely on the basis of `sender.participant_id`. This experimental version does not yet define a common identity-trust system across networks.

## 3. Intent structure

`intent.publish.payload` contains:

- `original_text`: the original expression, not replaced by an AI summary;
- `desired_outcome`: the result the user wants to achieve;
- `readiness`: `exploring` / `want` / `need` / `ready_to_purchase` / `committed_elsewhere`; none inherently creates a contractual obligation;
- `alternatives_acceptable`: whether alternative solutions are permitted;
- `user_confirmed`: whether the user has confirmed the AI interpretation;
- `constraints`: optional price, currency, time, region, quantity and technical parameters; missing values should not be guessed and treated as facts;
- `privacy`: an explicit sharing scope and optional permission for aggregate analytics;
- `interpretation_notes`: optional notes explaining AI inferences.

**A budget constraint is not a target for raising the price.** Servers SHOULD treat budgets as upper bounds or user-specified ranges when matching and analyzing needs, rather than guiding the system to push prices toward those bounds.

## 4. Proposal responses and explainability

`proposal.submit` supports `goods`, `service`, `custom_solution`, `non_transactional_solution` and `no_match`.

Proposals may specify:

- `satisfies`: which requirements are satisfied;
- `gaps`: which conditions are unmet or have not yet been verified;
- `pricing`: known goods, service, transport, tax and other costs; omit unknown costs rather than inventing zero cost;
- `source`: direct supplier information, an authorized API, user-entered information or another lawful source;
- `promotion`: whether sponsorship or commercial promotion is involved;
- `ranking_explanation`: the factors and explanations used for ranking, including whether commercial interests influence it.

Supply coverage must be explicit. Do not describe the best proposal found in a search as the best proposal in the world.

## 5. Independent outcome statuses

`outcome.report` requires separation of `need_status` and `transaction_status`:

| `need_status` | Meaning |
|---|---|
| `unknown` | It is not known whether the need is satisfied |
| `unmet` | Not yet satisfied |
| `partially_satisfied` | Partially satisfied |
| `satisfied` | Satisfied |

| `transaction_status` | Meaning |
|---|---|
| `none` | Unknown/no transaction recorded; it does not establish that no transaction occurred |
| `pending` | The transaction is still awaiting confirmation |
| `confirmed` | There is checkable confirmation |
| `cancelled` | The transaction was cancelled |

`evidence_source` must be stated: `user_confirmed` / `provider_confirmed` / `verified_record` / `inferred`. An `inferred` source cannot justify a claim that the buyer purchased something or that the need has been resolved.

## 6. Minimum requirements for the core network and routing

This experimental version does not define a mandatory global central directory. Implementers may find nodes through explicit address configuration, authorized directories, transport protocols agreed between the parties, or similar means.

Production transport requires its own security design. The experimental reference transport uses HTTP only on loopback, with JSON requests to `POST /odip/v0.1/messages`. It returns a core `receipt.ack` when the original message ID can be identified, and a structured error otherwise. Servers should apply request-body limits, timeouts, rate limits and auditable error logs to authenticated nodes. Successful network transmission cannot be equated with a completed transaction.

Minimum acceptance: two independently started nodes with separate data stores can exchange `intent.publish`, `proposal.submit` and `outcome.report`, with version validation, source verification, idempotency, rejection reasons and portable exports. The reference implementation must not secretly call an exclusive service operated by the initiator.

## 7. Existing e-commerce platforms, factories and third-party Agents

**Existing e-commerce platforms:** Taobao, JD.com and similar platforms may serve as lawfully authorized goods/service sources, with product cards linking to the original site for transactions. Whether they support ODIP is a separate fact; do not imply that they have already integrated. An open protocol does not grant rights to scrape or republish their data.

**Independent factories:** Forms, Excel or ERP adapters can declare capacity, minimum order quantities (MOQ), lead times and similar information; factories need not write ODIP packets manually.

**Third-party Agents:** May submit intents on a user's behalf, but must have appropriate authorization and minimum privileges, identify their sources and indicate the level of user confirmation. An Agent cannot complete an irreversible payment solely on the basis of its own inference.

**Identity is not tied to capability:** A logistics company provides a service when transporting goods and expresses demand when purchasing fuel. The protocol does not assign it a permanent role label.

## 8. Logistics and fulfillment extension

`fulfillment.quote` may provide transport capability, origin, destination, transport units, price, timing, insurance and special constraints for a proposal. A transport company may both offer quotes and express demand for return-load matching. A quote should be separate from an actual commitment to carry goods. Transport contracts, hazardous-materials permits and cargo-damage claims remain the responsibility of the actual operators.

**Compare total delivered cost:** Product price, transport, loading/unloading, insurance, taxes and necessary after-sales costs must distinguish known, unknown and not-applicable components. Do not omit logistics and then claim the lowest price.

## 9. Business models and charging boundaries (pricing outside the specification; disclosure within it)

The base ODIP protocol is free to use, and `extensions.commerce` is not mandatory. Commercial service operators may set prices, but must disclose the service, billing basis, trigger, recipient of payment, revenue-sharing recipients and refund-adjustment rules in advance.

- **0.35%** for operating a demand-side platform is a candidate business strategy, not a mandatory ODIP rate. It does not represent all costs including payments, taxes, guarantees, insurance or logistics.
- Agent-channel collaboration, such as `0.20%` for an operator and `0.15%` for a channel, is only an example of revenue sharing **after both parties agree**. It does not require every protocol-compliant transaction to pay the initiator.
- **For a single matching service, charge the same transaction unit only once.** Do not charge the same matching fee repeatedly on the entire original order value because production, transport, insurance, Agents or other participants are involved. Separately commissioned orders with distinct services may have separately negotiated prices, but the billing basis must be explicit and hidden duplicate charging is prohibited.
- Independently exchanging needs and completing transactions through ODIP outside a platform does not automatically grant the protocol initiator a right to charge. Separate obligations under existing valid contracts are excepted.
- Transaction value, channel commission and advertising fees must not be default weights for organic matching. Sponsored placements must be clearly identified and separated from organic ranking.

Revenue is not synonymous with protocol success: satisfying a need without a new transaction is also a positive outcome.

## 10. User data, demand intelligence and trustworthy statistics

Data falls into three categories:

1. **Users' original needs:** Must be collected and used lawfully; original text must not be sold externally without authorization.
2. **External supply data:** Access, cache and display it under the relevant source's license. `source` must be recorded, and `observed_at` SHOULD be recorded. Consumers must not guess freshness when the collection time is absent. The current experimental schema does not make collection time mandatory for every source.
3. **Platform-generated feedback and aggregate statistics:** Distinguish clicks, expressions of wanting, explicit needs, readiness to purchase, contract signing and actual completion, and avoid duplicate counting.

**Prefer statistics to guesses** does not mean **every expression can be counted as real purchasing power**. It is recommended to preserve sources, sample scope, deduplication methods, confidence/uncertainty statements and statistics dates. Shared aggregates should apply small-sample suppression and assess re-identification risks. Handle deletion or withdrawal under published retention rules and legal requirements.

## 11. Security, trust and boundaries

- Schema validation in this version **does not establish** real identity, compliance or a transaction guarantee.
- Implementations must defend against malicious messages, replay, privacy leaks, fabricated transactions, fake suppliers, poisoning and unauthorized transactions by Agents.
- A production network should have independent identity verification, fine-grained authorization, rate limits, auditing, key rotation and abuse appeals. Do not claim secure global routing before the necessary extensions are completed.
- Automated revenue sharing, guarantees, payments, loans, smart contracts and arbitration **are not part of the core standard**. They require separate design, regulation and testing.

## 12. Versioning, compatibility and community governance

- `0.x` identifies an experimental draft and permits breaking changes, but each change MUST include migration guidance.
- Core objects use closed field sets. Adding a core field also requires an explicit version revision. Only unknown non-critical extensions within `extensions` may be ignored; old core schemas are not promised to accept new fields automatically.
- Unknown non-critical extensions may be ignored; unknown core messages must be explicitly rejected.
- Public PR/RFC discussions should record motivation, alternatives, compatibility effects and tests.
- Maintainers may not change basic interoperability or automatically impose a protocol tax for the initiator's commercial benefit.

## 13. MVP acceptance and exclusions

**First useful demonstration:** A consumer writes, “It is unsafe for my parents to use a kitchen knife.” AI only assists structuring and preserves the original words. Node A publishes the need; node B returns both a product candidate and a way to solve it without buying a new product. After the user selects an outcome, an `outcome.report` is produced. Even with `transaction_status=none`, `need_status=satisfied` is possible.

**Required before release:** Schemas and examples validate; two independent nodes interoperate locally; fields and message versions are consistent; open-source licenses, contribution rules, commercial boundaries and migration guidance are complete; privacy defaults can be inspected.

**Outside the first version:** Global financial clearing, a universally valid supplier-credit system, real cross-border compliance, exhaustive product data from all platforms, unrestricted crawling, automatic transaction commitments, mandatory central discovery and platform-level fairness certification.

## 14. Future extensions (not release blockers)

- Standardized capability discovery and cross-organization node authentication;
- Product adapters and factory ERP integration;
- The `odip-fulfillment` logistics-capability extension;
- `odip-commerce` fee disclosure and contract references;
- Demand-group aggregation, privacy protection and sampling corrections;
- Reproducible tests of fair ranking, feedback and appeals;
- Research into specialized funds, insurance, financing and related extensions only when real use cases arise.

**Final principle:** Demand first, role neutrality and collaboration that creates value. The protocol does not control transactions; services earn fees through their value.

## 15. Experimental conformance rules for independent implementations

This section and the local [packet schema](schemas/packet.schema.json) together define the experimental machine-exchange contract. Schema `required`, `enum`, length limits and closed field sets are normative constraints. Schema `$id` values use `example.invalid` only to identify resources; validation MUST use the repository's local files and must not make network requests because of those identifiers. Report conflicts between prose and schemas as specification defects; no implementation may silently decide the matter on its own. The following rules specifically resolve uncertainties found in the baseline.

### 15.1 Conformance layers and structural rules

An implementation claim MUST state its version and supported layers: `schema` (packet structure), `semantic` (relations within one packet), `stateful` (message history), and `loopback-transport` (local experimental transport). Supporting one layer does not substitute for verification of others. The core requires seven message types. `fulfillment.quote` and `commerce` are separately optional; implementations claiming support must validate their rules. The current suite can test all eight message types supported by the reference implementation. An implementation without optional functionality must explicitly report it as unsupported and cannot claim to have passed the full suite.

| ID | Constraint | Failure |
|---|---|---|
| S-01 | MUST validate JSON Schema Draft 2020-12 with `uuid` and `date-time` format assertions enabled; the root must be an object, with no additional core fields | `SCHEMA_INVALID` |
| S-02 | The six need-related message types publish/update/withdraw/proposal/outcome/fulfillment MUST include `intent_id`, 1–128 characters, compared as an exact string | `SCHEMA_INVALID` |
| S-03 | `protocol` MUST be exactly `ODIP/0.1.3-exp.1`; no guessing or implicit downgrade | `VERSION_UNSUPPORTED` |
| S-04 | Every field defined as `date-time` MUST use a valid Gregorian date, 24-hour time, uppercase `T` and `Z`, such as `2026-11-04T03:00:00.123456Z`; the fractional part is optional and has 1–6 digits when present. Offsets, leap seconds, missing time zones and invalid dates are not accepted | `SCHEMA_INVALID` |
| S-05 | A rejected `receipt.ack` MUST carry a nonempty `reason_code`; accepted/duplicate do not require a reason | `SCHEMA_INVALID` |
| S-06 | An implementation claiming commerce support MUST validate the inline structure of `extensions.commerce`; the standalone extension schema and inline definition have the same meaning | `SCHEMA_INVALID` |
| S-07 | Unknown non-critical members of `extensions` MAY be stored, but their business effects MUST be ignored. They must not change core semantics, execute content, automatically access contained URLs or elevate privileges | Do not reject solely because of an unknown non-critical extension |

UUID fields MUST be canonical lowercase hexadecimal UUID strings with the 8-4-4-4-12 hyphenated format, to prevent case variants of the same UUID from creating different idempotency keys. Intent, proposal and participant IDs are opaque strings; do not infer real identity or organizational affiliation from their appearance. Participant, intent and proposal IDs are each limited to 128 Unicode characters. A message ID is unique within the receiving node's persistent message domain. Critical-extension negotiation is not currently defined: an unknown extension cannot be declared critical with a claim that the peer understands it. New critical semantics require agreement on a new protocol version first.

`gaps`, `satisfies`, `pricing` and `source.observed_at` are optional. Omitting `gaps` means undisclosed, not that there are no gaps. Omitting a price means unknown, not zero cost. `promotion.sponsored=true` should explain the promotional influence. `source.kind` and `evidence_source` are sender declarations; they do not automatically become facts verified by a third party.

### 15.2 Single-packet semantic rules

| ID | Constraint | Error code |
|---|---|---|
| M-01 | When `payload.target_intent_id` is present, it MUST exactly equal the envelope's `intent_id` | `ID_MISMATCH` |
| M-02 | With `evidence_source=inferred`, the packet MUST NOT claim `transaction_status=confirmed` and MUST NOT claim `need_status=satisfied` or `partially_satisfied` | `INFERRED_ASSERTION` |
| M-03 | `transaction_status=confirmed` MUST include a non-blank `evidence_note` explaining the basis of checkable confirmation. This checks completeness of a declaration; the receiver must still independently verify the evidence's truth | `EVIDENCE_REQUIRED` |
| M-04 | In this experimental version, commerce `share_rate` values are ratios of the same `fee_basis`. Beneficiary identifiers MUST be unique, and their exact decimal sum MUST not exceed `fee_rate`. Any unallocated remainder does not automatically belong to anyone | `COMMERCE_INVALID` |
| M-05 | `consent_recorded=false` means consent has not been recorded; it may still be exchanged as a disclosure without recorded consent. A true value is also only a declaration. Disclosures, receipts and status values MUST NOT automatically create a payment, revenue share, mandatory commission or contractual commitment | No charging action |

`fee_rate` and `share_rate` use 1 to mean 100% and 0.0035 to mean 0.35%. Revenue-share arithmetic MUST use decimal numeric meaning; binary floating-point error must not cause rejection of 0.002+0.0015=0.0035. `fee_basis` and `charge_trigger` are disclosure text, not executable expressions. There is no rule multiplying the total rate by the participant count. Machine-executed billing quantities or amount formulas for `fixed_fee`, `subscription` and `usage_fee` are not currently defined; this version validates only their disclosure structures. Passing the tests alone cannot justify any implementation's claim to a right to charge.

`need_status` and `transaction_status` do not imply one another. For example, satisfied+none and unmet+confirmed can both be valid; the latter still requires the confirmation-basis rule. A readiness of ready_to_purchase does not produce a confirmed transaction either.

### 15.3 Stateful experimental profile

This is an explicit, strictly ordered profile for reproducible verification, not a distributed consensus protocol. Implementations MAY use any storage form. The following specifies external behavior, not a requirement to copy the reference database.

| ID | Input and preconditions | Successful state change / rejection |
|---|---|---|
| ST-01 | intent.publish with a new `intent_id` | Store the publisher as owner, revision=1 and active=true; an existing ID returns `INTENT_EXISTS` |
| ST-02 | intent.update; target exists and is active; sender is owner; revision=current+1 | Store the complete new intent and revision, preserving the historical original text. Unknown target: `UNKNOWN_INTENT`; non-owner: `FORBIDDEN`; nonconsecutive revision: `REVISION_CONFLICT` |
| ST-03 | intent.withdraw; target exists and is active; sender is owner | Set active=false; withdrawal does not cancel external contracts or mean that historical records have been deleted |
| ST-04 | proposal.submit; target exists and is active; new proposal_id | Store the proposal bound to the intent; duplicate proposal ID: `PROPOSAL_EXISTS`. Offering a capability does not create a permanent seller identity |
| ST-05 | outcome.report; target exists and is active; sender is owner | Store the report without automatically changing intent activity, initiating a payment or closing an external transaction |
| ST-06 | fulfillment.quote; target exists and is active; proposal already exists and belongs to the same intent | Store the quote; unknown proposal: `UNKNOWN_PROPOSAL`; inconsistent association: `ID_MISMATCH`. A quote is not a transport commitment |
| ST-07 | receipt.ack referencing an outbox message locally sent to this authenticated peer | Record the receipt status; if that ID/peer sending relationship does not exist, return `UNKNOWN_MESSAGE`. As a response to one HTTP delivery, it must also bind to the original message ID of that delivery |

Except for initial publication, need-related inputs first check whether the target exists. Operations requiring the owner then check identity, followed by active status. After withdrawal, when identity/permission requirements are satisfied, new update, withdraw, proposal, outcome and fulfillment messages all return `INTENT_WITHDRAWN`. Restoring a withdrawn need requires explicitly creating a new intent; there is no implicit revival operation. This is a restriction introduced by the experimental profile, not evidence that v0.1.2 already had a common state machine. capability.advertise has no intent-state precondition. Its validity-period declaration is not proof of qualification; callers still verify actual capability.

Each accepted message and its state change MUST be persisted atomically; accepted may be returned only after commit. Rejected messages MUST NOT change business state. The receiving idempotency table, accepted raw messages, intent revisions and proposal associations must survive restart. Before sending a new message, a client MUST save the raw outbox request bytes and destination, and save local sending state so that incoming proposals can be related to its own published intents. Recording a sent message locally does not establish that the peer received it; after failure, retry and validate the receipt.

Out-of-order messages are explicitly rejected rather than queued indefinitely. After supplying missing predecessors, the sender may retry the original packet. Timestamps express source time and do not replace revisions, unique IDs or authorization order; this version does not require causality to be inferred from wall-clock order. Currently only the owner can modify, withdraw or report on its own intent. Cross-organization delegated authorization and combining outcomes from multiple actors are not defined. Future extensions must preserve real provenance and must not impersonate the owner.

### 15.4 Privacy and authorization profile

P-01: Original text with `sharing_scope=private` MUST NOT be transmitted between nodes; the reference network receiver also returns `PRIVACY_DENIED`. For `selected_participants`, the sender MUST check each destination against an explicit local allowlist. This restriction also covers proposals, outcomes, withdrawals, fulfillment and other messages related to stored intents; it is not sufficient to protect initial publication while allowing derived data to flow freely. A public scope still does not grant rights to unrelated processing, selling original text or re-identification. A receiver can only check that the sender is an authenticated peer; the packet alone cannot prove real user authorization, so an implementation cannot claim to have verified its authenticity. Intents without a sharing scope are rejected by the schema; no public default is supplied. `allow_aggregate_analytics=false` MUST NOT be interpreted as permission to aggregate. A true value does not waive de-identification or re-identification risk assessment.

P-02: Test identity and production identity MUST be declared separately. The experimental profile binds transport identity to `sender.participant_id` through a local peer→test-token mapping; a mismatch returns `SENDER_MISMATCH`. This authenticates two test processes, not the existence of an organization, authority to act as an Agent, contractual authority or production-network security. Capability enumerations do not determine permanent business roles. Implementations must not automatically retrieve evidence from message URLs, execute extension scripts, or leak tokens or complete private needs into diagnostic logs.

P-03: Preserving original words requires historical integrity within the scope of authorized storage; it cannot be used to deny deletion rights. The prototype retains history to verify recovery and does not yet provide automatic deletion, withdrawal propagation or retention-period negotiation. Real personal-data processing requires separate design and review first. Test identities and data are synthetic and cannot be advertised as real third-party integrations.

### 15.5 Local transport, idempotency and recovery

T-01: The local experimental interface is loopback HTTP `POST /odip/v0.1/messages`, with `Content-Type: application/json` and a UTF-8 request body without a BOM. It is not a production HTTPS security configuration and must not bind to a public interface. Authentication comes from configured test-peer tokens; public example identity IDs are not credentials. JSON MUST reject duplicate keys, NaN/Infinity, invalid UTF-8 and trailing non-whitespace content. Object-key order and whitespace do not affect schema meaning, but do affect the retry byte identity below.

T-02: In this experiment, “same ID, same content” means exactly **identical raw UTF-8 request-body bytes**. The receiver stores the original bytes or their SHA-256 bound to `message_id`. The same ID and bytes return duplicate without applying state again; the same ID with different bytes returns `ID_CONFLICT`. Duplicates of accepted messages must be handled before reapplying state transitions, so later withdrawal of an intent must not turn replay of an originally successful packet into failure. This is a portable byte contract, not JSON canonicalization: changing whitespace, key order, or 1 to 1.0 causes a conflict. Sender retries MUST reuse the original outbox bytes, without reserializing or refreshing timestamp. Modified content requires a new message ID.

T-03: No response does not establish that a message was not received. The client retries the same packet, while the receiver responds after durable commit, preventing duplicate application when commit succeeded but the response was lost. Failure may report TIMEOUT or a connection error; the outbox is not deleted. Clients can resume retry after restart, and receivers retain the original idempotency table. Duplicate-delivery verification demonstrates at-most-once state application and retryable reception, not network-wide exactly-once behavior or a guarantee of transaction completion.

Every send and retry MUST recheck the current destination configuration and authorization for outbound disclosure. Persisting an old packet does not freeze future sending permissions. If the peer has been removed or selected authorization revoked, return UNKNOWN_PEER or PRIVACY_DENIED locally, do not connect, and mark the outbox entry blocked. Batch retry skips blocked entries. After restoring authorization, an operator can explicitly send the original packet. Authorization blocking takes precedence over delivery recovery. If only the need has subsequently been withdrawn and disclosure authorization remains valid, an originally accepted historical packet can still be retried idempotently, without applying state again.

T-04: Application results for valid requests use `receipt.ack`, whose payload contains the original message UUID and accepted/rejected/duplicate status. The receipt's own message ID must be a new UUID, its sender must be the responding node, and its timestamp must use this version's UTC format. It must not copy the original packet's sender as its own. A request without a valid message UUID requires a structured transport-layer error rather than a fabricated correlatable receipt. The client MUST check the response version, schema, sender, original_message_id and current delivery destination. An invalid response cannot mark the outbox as delivered. A receipt acknowledges processing, not factual truth or satisfaction of the need.

HTTP 200 MUST correspond to an accepted/duplicate receipt. A 4xx business rejection MUST correspond to a rejected receipt. Transport errors before parsing may use an error object with nonempty code/reason, and HTTP must indicate an error status. Any contradiction between status and content is INVALID_RECEIPT, leaving the outbox pending. Do not interpret an error object under a false 200 as valid success. HTTP 408, 429 and 5xx are retryable transport failures and do not establish that business state was not committed.

T-05: Implementations MUST limit message-body size, JSON depth, read timeouts and connection handling, and must not automatically follow URLs in messages. Resource limits belong to transport configuration; arbitrary extra schema limits on every business field are not a substitute. Exceeding a limit must cause explicit rejection without persistence of business state. Rate limits and timeouts do not establish denial-of-service security certification. See the running tutorial and security documentation for reference settings and test commands. Unknown core messages must be explicitly rejected; their presence does not imply that a central node service is required.

The reference local profile fixes the maximum message body at 65,536 bytes and maximum JSON depth at 32 (root depth is 1, increasing by 1 at each level), and rejects isolated UTF-16 surrogates. The absolute value of the exponent after decimal-number parsing is limited to 10,000; larger exponents return INVALID_JSON to prevent extreme numbers from exhausting resources. These are runtime boundaries, not changes to the numeric meaning of core business fields. The server has a 2-second per-connection read timeout, at most 8 handling workers and a pending-connection queue of 8. Each authenticated peer is limited to 120 requests per minute, using an in-memory sliding window cleared on restart. The default client timeout is 2 seconds; it can be configured above 0 and at most 10 seconds. There are no automatic background retries; explicit retry replays persisted original bytes. These are settings of this experimental transport, not universal Internet-security thresholds.

Reference HTTP statuses: success 200; authentication failure 401; permission/privacy rejection 403; unknown path 404; same ID with different bytes 409; request too large 413; rate limit 429; read timeout 408; other packet errors 400. When no valid UUID can be associated, respond with `{"error":{"code":"...","reason":"..."}}`; otherwise respond with a rejected receipt. HTTP status does not replace receipt validation. A client does not automatically send another receipt after receiving an HTTP receipt, avoiding acknowledgement loops. A manually POSTed receipt may receive one response, but still does not trigger recursive acknowledgements.

Runtime error codes also include INVALID_JSON (invalid encoding, JSON or numeric resource bounds), DEPTH_LIMIT, MESSAGE_TOO_LARGE, AUTH_REQUIRED, SENDER_MISMATCH, CONTENT_TYPE, CONTENT_LENGTH, UNSUPPORTED_ENCODING, NOT_FOUND, RATE_LIMIT and TIMEOUT. Local client failures may report CONNECTION_FAILED, UNKNOWN_PEER, REMOTE_RETRYABLE and INVALID_RECEIPT; these are not transaction outcomes. When the concurrency limit is reached, or a timeout occurs before complete request headers arrive, the connection may close without a message receipt. The client must treat this as unconfirmed delivery and cannot infer that nothing was committed. Error explanations must not echo secrets, tokens or complete private original text.

### 15.6 Public tests and result claims

[conformance/manifest.json](conformance/manifest.json) is a language-independent test manifest containing per-packet structural/semantic vectors and ordered state vectors. Each case declares its rule and expected result. Implementers may reconstruct validators and storage in any language and publish their test results, but cannot use calls into the reference implementation as evidence of an independent implementation. The corpus demonstrates only the cases it covers, not coverage of every valid input or all production risks.

Implementation claims MUST separately state: passed schema validation, passed local independent-process verification, passed real-network security verification, passed cross-implementation interoperability verification, and not yet verified. Unexecuted layers must be marked “not yet verified.” Two processes using the same codebase support only the second claim, not cross-implementation or cross-organization interoperability claims.
