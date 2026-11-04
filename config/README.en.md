# Configuration boundaries

[简体中文](README.md) | **English**

Configuration is generated locally only: `python scripts/prepare_local.py` writes to the Git-ignored `runtime/manual/` directory.

Configuration fields:

- `participant_id` is the local test identity.
- `peers` maps peer IDs to a `url` and a random `token`.
- `selected_recipients` is an explicit list of recipients allowed to receive `selected_participants` intents.

URLs are restricted to `http://127.0.0.1:port`. Tokens are for testing only, not production credentials or an identity system.

Do not commit generated tokens, configuration, databases or exports. There is no preconfigured universal shared password. Do not change other projects or global configuration. Configuration files are supplied by the local operator and must not be loaded dynamically from untrusted messages.
