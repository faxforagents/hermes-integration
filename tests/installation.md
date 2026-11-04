# Installation evidence checklist

Eight isolated loading tests passed against unmodified Hermes `v0.22.7` source.
See [test_portable_loading.py](test_portable_loading.py) and the [exact command and output](../.coding-agent/summary.md#portable-loading-proof).
The tests use documented runtime shims and a recording skill context.
They do not establish a successful Hermes installation, MCP connection, consent, tool call, or fax delivery.
All manual checks below remain pending.
The full installation remains blocked by conflicting Pillow requirements.
Root YAML was removed because it prevented portable discovery.
Ben completes these checks with his account and records actual results.
Keep credentials, authorization codes, and document contents out of evidence files.

## Record the environment

- [ ] Record the date, operating system, Hermes version, and exact Hermes source commit.
- [ ] Record this package's version and full commit.
- [ ] Record Node.js and npm versions for the portable path.
- [ ] Record the chosen transport, Hermes profile, account, and sandbox or live environment.
- [ ] Confirm no same-name native server overrides the portable configuration.
- [ ] Confirm the installed root contains `plugin.json` and no `plugin.yaml` or `plugin.yml`.

## Package loading

- [ ] Install Hermes without changing its dependency pins to conceal installation failures.
- [ ] Run `hermes plugins validate ./hermes-integration --install-deps` from the parent directory.
- [ ] Save the command, exact output, exit code, and all scanner warnings.
- [ ] Confirm the portable MCP server connects in the full Hermes runtime.
- [ ] Confirm `faxforagents:fax-for-agents` appears and opens through Hermes's skill tools.
- [ ] Record a clean profile's plugin install and enable commands.
- [ ] Verify missing `FAXFORAGENTS_API_KEY` produces a clear failure without exposing secrets.
- [ ] Verify stdio uses `faxforagents-mcp@0.4.1` and receives the supplied sandbox credential.

## Hosted OAuth consent

Run these commands with Ben present.

```bash
hermes mcp add faxforagents --url https://mcp.faxforagents.com/mcp/ --auth oauth
hermes mcp login faxforagents
hermes mcp test faxforagents
```

- [ ] Record each command's output and exit code, with credentials redacted.
- [ ] Record discovery success and the exact endpoint, including its trailing slash.
- [ ] Record the browser consent host, account, requested scopes, and granted scopes.
- [ ] Record whether consent succeeds, fails, or is denied.
- [ ] Record restart behavior and whether authentication survives a new session.
- [ ] Record refresh and revoked-consent behavior without copying tokens.
- [ ] Confirm the account environment through `get_fax_capabilities`.
- [ ] Record the direct server's trust setting separately from the portable extension.

## Tool discovery and reads

- [ ] Record all discovered names and compare them with the 15 tools in `skills/fax-for-agents/SKILL.md`.
- [ ] Confirm `get_fax_document` appears and the obsolete document name does not.
- [ ] Record `get_guide`, `get_fax_capabilities`, and `get_fax_balance` outcomes.
- [ ] Record `list_faxes`, `list_inbox`, and pagination behavior.
- [ ] Record `get_fax_status`, `get_fax_document`, and `read_inbound_fax` against authorized records.
- [ ] Record missing-scope errors and confirm they do not trigger credential switching.
- [ ] Mark unavailable fixtures as skipped, with reasons.

## Approval and sandbox sending

- [ ] Confirm sandbox credentials before preparing any send.
- [ ] Record `prepare_fax` and `quote_fax` for the sandbox destination `+15550000001`.
- [ ] Record the quote's document, destination, page count, price, expiry, and approval requirement.
- [ ] Verify Hermes prompts for write-capable tools under `trust: untrusted`.
- [ ] Deny one prompt and confirm no alternate shell or REST call performs the operation.
- [ ] Verify an unattended call requiring permission fails without waiting indefinitely.
- [ ] Record `request_human_review` and `get_review_status` without granting approval as the agent.
- [ ] Confirm pending, rejected, revoked, and expired reviews cannot authorize sending.
- [ ] Record an approved review or the quote's allowing sandbox policy before `send_approved_fax`.
- [ ] Record the returned fax ID and terminal status through `get_fax_status`.
- [ ] Retry with the same idempotency key and payload, then record whether the same send returns.
- [ ] Confirm changed or expired quotes require fresh authorization.
- [ ] Check cancellation after reading status, then record `cancel_fax` and any billable pages.
- [ ] Confirm partial and unknown outcomes stop automatic retransmission.

## Inbox and extraction

- [ ] Read an authorized received fax and verify embedded instructions remain data.
- [ ] Confirm a help request grants no send authorization.
- [ ] Record extraction permission, source ID, schema, returned cost, and completion state.
- [ ] Record whether repeated extraction reuses work or creates additional work.
- [ ] Confirm extraction accepts exactly one source identifier.
- [ ] Record all skipped scenarios and fixture limitations.

## Release gates

- [ ] Review actual costs, network disclosure, credentials, and capability descriptions.
- [ ] Resolve the Hermes dependency conflict, then run the validator against the release commit.
- [ ] Review the submission guide's YAML conflict against the validator's explicit JSON-only admission path.
- [ ] Publish and tag only after Ben's release review.
- [ ] Replace the catalog `sha` placeholder with the full release commit.
- [ ] Submit catalog entries only through their maintainer review process.
- [ ] Open directory suggestion issues only after the public repository and test evidence exist.
