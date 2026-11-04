# Reference nodes in independent processes

[简体中文](REFERENCE.md) | **English**

This tutorial uses only synthetic data, loopback HTTP and temporary test credentials. The two nodes use the same Python implementation, with separate processes and SQLite storage. After preparing the [environment](ENVIRONMENT.en.md), the shortest command for generating evidence is:

```powershell
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/demo-02 --report evidence/two-process-evidence.json
```

The report records actual server process IDs, ports, request SHA-256 values, receipts, restarts and statistics from the separate databases; it does not print tokens. The test controller sends byte requests, reads health status and checks database evidence. It does not transfer business state directly between the nodes or share Python objects on their behalf.

## Start the nodes manually

First generate fresh configuration from the root of the extracted or checked-out repository:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_local.py
```

Terminal A:

```powershell
.\.venv\Scripts\python.exe -m odip.node serve --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --port 8761
```

Terminal B:

```powershell
.\.venv\Scripts\python.exe -m odip.node serve --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --port 8762
```

In a third terminal, send the following messages in order. The sending CLI shares **its own node's** database with that node's server; it does not share a database with the other node.

```powershell
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --peer test-node-b --message runtime/manual/intent.publish.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --peer test-node-a --message runtime/manual/proposal.goods.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --peer test-node-a --message runtime/manual/proposal.nontransaction.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --peer test-node-b --message runtime/manual/outcome.no_purchase.json
```

Each HTTP response is a schema-defined `receipt.ack`; it does not establish a transaction or certify facts. Sending the same unmodified file again returns `duplicate`; changing its content while retaining the same ID is rejected. Restart B with its database preserved, then resend the original file: it is still a `duplicate`.

## Recover from failure and export data

A connection failure or timeout leaves the message in the durable outbox. After restoring the peer, run:

```powershell
.\.venv\Scripts\python.exe -m odip.node retry --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3
.\.venv\Scripts\python.exe -m odip.node export --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --output runtime/manual/export.json
```

Retries use the original UTF-8 bytes without reformatting the message. If a successful receipt is lost, retrying should receive `duplicate` and complete the outbox entry. A permanent rejection retains a `rejected` record rather than retrying indefinitely. The operator must understand the reason and may explicitly send the original file again after correcting prerequisite state or configuration, or construct a new message for the current revision state. Local sending state does not automatically roll back when the remote node rejects a message.

The export destination must not already exist. It contains authorized local data and is not served over the network by default. This prototype has no import, deletion or retention-period management, and does not claim complete data migration or enforcement of privacy withdrawal.

Messages must pass byte-level, schema, cross-field semantic, current-state and authorization checks. A `private` intent cannot be sent across nodes. Authorization for selected recipients is configured by the operator; the declaration itself cannot prove real user consent. Unknown extensions have their business meaning ignored as specified; the known commerce extension is validated but never executes charges.

Stop a node with Ctrl+C. Do not expose public-network ports, create tunnels or treat this HTTP/static-test-token mechanism as a production security solution. See the [security model](SECURITY.en.md).
