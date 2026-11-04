# Security model and known limitations

[简体中文](SECURITY.md) | **English**

Scope: the `ODIP/0.1.3-exp.1` local experimental reference implementation. It uses only simulated participants and synthetic data; it must not be described as third-party organizational adoption, actual user authorization, production security or Internet certification.

## Trust boundaries

Protocol declarations, receiver-side validation and real-world facts are three different levels of evidence. A schema can validate field structure. The semantic layer can reject contradictions between `inferred` and `confirmed`/`satisfied`. Neither can verify that a user actually consented, a supplier really exists, a referenced record is genuine, authorization is valid or a transaction was fulfilled.

Reference nodes are hardcoded to bind to `127.0.0.1`. Senders accept only an `http://127.0.0.1` base URL with an explicit port, do not follow redirects and do not use a designated central service. Plaintext HTTP is a transport convention for local testing. There is no TLS, certificate validation, cross-organization trust or confidential-transport guarantee. Using TCP/IP or passing a two-process test must not be described as passing real-network security validation.

Authentication uses bilateral random test tokens in configuration, bound to the peer's `participant_id`. The message's self-declared `sender` must match the principal authenticated through configuration. Each peer token contains at least 32 ASCII alphanumeric characters and is generated at test runtime. Configuration files and databases stay out of Git. This authenticates the holder of a test secret, not an organization, person, Agent delegation or qualification to transact.

## Implementation controls and limits

| Threat or boundary | Experimental control | Not yet covered |
|---|---|---|
| Forged `sender` | Bind token to peer; compare the authenticated principal with `sender` | Public keys/certificates, real identity, rotation, revocation and delegation chains |
| Unauthorized intent changes | The publisher has update/withdraw/outcome permissions; ordered revisions and a terminal withdrawn state | Shared ownership, authorized proxies and merging multiple writers |
| Duplicates and replay | SQLite durably stores `message_id`, original UTF-8 bytes and their digest; the same ID with identical bytes is a duplicate, different bytes are a conflict; receipts follow the database transaction | Global uniqueness, indefinite replay protection and cross-node deletion synchronization |
| Lost receipts or disconnection | Store the outbox before sending; explicit retry reuses the same bytes and ID | Automatic scheduling, operational backoff queues and distributed exactly-once processing |
| Confused associations | Check intent, proposal and receipt relationships, provenance and state | External database facts and interpretation of business contracts |
| Untrusted JSON | 65,536-byte limit, depth 32; reject duplicate keys, invalid UTF-8, non-finite numbers and malformed JSON | Comprehensive fuzzing and analysis of differences among language parsers |
| Slow requests or resource exhaustion | 2-second socket timeout, at most 8 worker threads, queue size 8, 120 requests per peer per minute; encoding and length limits | Public-network DDoS, host-wide isolation, persistent database capacity/disk quotas and multi-tenant SLAs |
| Sending private content | `private` cannot cross nodes; `selected_participants` allows only explicit local recipients; no aggregate analysis is executed | Evidence of the other party's consent, purpose controls, onward sharing after receipt and prevention of re-identification |
| Information leakage through errors | Structured generic error codes and rejection reasons; runtime logs do not print message bodies, tokens or exception traces for malformed requests | Log-retention audits, endpoint-metadata concealment and malicious administrator access |
| Commercial extensions | Validate known commerce fields, rates and allocation constraints; disclosure only | Actually authorized charging, payments, taxation, allocation execution and real duplicate-charge audits |
| Extension abuse | Unknown non-critical extensions are not executed and do not alter core semantics | A global extension registry, negotiation of critical extensions and executable-plugin sandboxes |

In this transport experiment, “identical content” for idempotency means identical bytes of the complete original UTF-8 request body. Changes to whitespace, key order or numeric lexical representation also cause a conflict; this is not a general JSON canonicalization algorithm. Senders must retain the bytes to retry rather than reserialize a message and reuse its ID.

`/health` exposes process and simulated participant information on the loopback address for readiness checks; it should not be exposed to the public Internet. The Python standard HTTP server is used for readable reference code, not as a hardened production server. Concurrency beyond the worker limit may result in a connection being closed directly. Clients should treat that as a retryable transport failure rather than expect a protocol receipt for every overload condition.

## Data lifecycle

The database retains complete received/sent messages and old revisions for idempotency and traceability of original wording. Withdrawing an intent is a business state, not physical deletion. There is currently no automatic expiry, encrypted storage, backup rotation, proof of remote revocation or implementation of legally required deletion. Use only synthetic data; do not enter real personal information or actual commercial records into this prototype.

Export uses an explicit local CLI to write a new file. There is no unauthenticated network export endpoint; operators with local file permissions can read the data. Export does not broaden the original authorization. Operating-system accounts, ACLs, disk encryption and backup security are controlled by the operator. This work did not independently validate Windows ACLs or administrator attacks.

## Still requiring independent validation

Public-network HTTPS, real authentication and authorization, key management, abuse prevention, penetration testing, supply-chain vulnerability audits, cross-language parsing consistency, multi-organization interoperability, real provenance evidence and compliance with privacy laws all remain unverified. Third-party independent implementations may run the public test suite, but must identify their implementation, version, platform and evidence separately. Self-testing the reference implementation does not establish interoperability between independent implementations.

Report sensitive findings under the repository's [security policy](../SECURITY.md), using a private reporting entry point that is actually available. If it is unavailable, do not disclose details publicly; ask for a usable private contact without including sensitive information. This document does not provide a fabricated email address or response SLA, and does not assume that a repository or fork has enabled private reporting merely because it contains this document.
