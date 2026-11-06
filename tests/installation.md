# Installation evidence

Eight isolated loading tests passed against unmodified Hermes `v0.22.7` source.
See [test_portable_loading.py](test_portable_loading.py).
The tests use documented runtime shims and a recording skill context.
They do not establish a Hermes installation, an MCP connection, consent, a tool call, or a fax delivery.
The manual checks below record what was run on a real Hermes 0.22.7 install.
Unchecked items were not run.
Authorization codes are masked in the outputs. Nothing else is edited apart from removed terminal colour codes.

## Environment

- [x] Date: 2026-11-04 to 2026-11-06. Host: `work-horse`, Ubuntu 24.04.5 LTS, x86_64.
- [x] Hermes Agent v0.22.7 (2026.9.24), git install at commit `b200f5bc60e31588ba2cb60e288029c4a54ba5fa` (2026-11-03), installed with the official installer. Python 3.14.9 (Hermes's own interpreter), mcp SDK 2.3.0.
- [x] Package: this repository at the `v0.1.1` release commit.
- [ ] Node.js and npm versions for the portable path: the portable stdio server was not launched inside Hermes.
- [x] Transport: Streamable HTTP with OAuth against the sign-in URL `https://mcp.faxforagents.com/mcp/?auth=required`. Default Hermes profile. Fax for Agents account of the maintainer, sandbox environment.
- [x] No same-name native server overrides the portable configuration: the native `faxforagents` server is the only one configured, the portable plugin was not installed into this profile.
- [x] The package root contains `plugin.json` and no `plugin.yaml` or `plugin.yml`.

## Package loading

- [x] Hermes installed without changing its dependency pins. A pip build fails on a Pillow pin conflict with browser-harness and Hermes refuses it by design. The official installer provisions its own environment and works.
- [x] `hermes plugins validate ./hermes-integration --install-deps` ran on 2026-11-04 from the parent directory of a clean `git archive` export of the package. Exit code 0.

```
✓ portable manifest — plugin.json parses (Agent Plugins v1)
✓ manifest fields — name present
✓ config schema — not declared
✓ server trust: faxforagents — untrusted (Hermes asks before every write-capable
tool call)
✓ security scan — safe
◆ Isolation — portable plugin (no Python): runs anywhere

Validation passed.
```

- [ ] Portable MCP server connecting in the full Hermes runtime: not run.
- [ ] `faxforagents:fax-for-agents` appearing through Hermes's skill tools: not run.
- [ ] Clean profile plugin install and enable commands: not run, the catalog entry waits for review.
- [ ] Missing `FAXFORAGENTS_API_KEY` failure: not run.
- [ ] stdio with `faxforagents-mcp@0.4.1` and the supplied sandbox credential: not run.

## Hosted OAuth sign-in

### Plain URL, 2026-11-04

The plain URL `https://mcp.faxforagents.com/mcp/` answers anonymous `initialize` with 200. Hermes connected without a token and found all 15 tools:

```
Script started on 2026-11-04 15:22:21+02:00 [COMMAND="hermes mcp add faxforagents --url https://mcp.faxforagents.com/mcp/ --auth oauth" <not executed on terminal>]

  Starting OAuth flow for 'faxforagents'...
  ✓ OAuth configured (tokens will be acquired on first connection)

  Connecting to 'faxforagents'...

  ✓ Connected! Found 15 tool(s) from 'faxforagents':

    get_guide                       Read the Fax for Agents manual and tool workflow. Start here...
    get_fax_capabilities            Read account limits, routes, formats, prices and credential ...
    prepare_fax                     Create a fax document from text, Markdown, HTML or a complet...
    get_fax_document                Read one fax document and its page previews. Use the documen...
    quote_fax                       Price one prepared document for one fax destination. Use aft...
    send_approved_fax               Queue one quoted outbound fax for delivery. Use after quote_...
    get_fax_status                  Read one outbound fax's delivery state and attempts. Use aft...
    list_faxes                      List outbound faxes your organization sent, newest first. Us...
    get_fax_balance                 Read available and held wallet funds in the credential's env...
    cancel_fax                      Request cancellation of one outbound fax. Use get_fax_status...
    request_human_review            Ask a person to approve a quoted send or help with a fax. Wi...
    get_review_status               Read the human approval decision for one review request. Use...
    list_inbox                      List received faxes on your organization's numbers, newest f...
    read_inbound_fax                Read one received fax with its page count, document referenc...
    extract_fax_data                Start or retrieve OCR and optional structured field extracti...

  Enable all 15 tools? [Y/n/select]: Y

  ✓ Saved 'faxforagents' to ~/.hermes/config.yaml (15/15 tools enabled)
  Start a new session to use these tools, or run /reload-mcp to load them into open sessions.

Script done on 2026-11-04 15:27:21+02:00 [COMMAND_EXIT_CODE="0"]
```

`hermes mcp login faxforagents` then ended without a sign-in. Production logs show no request to the registration or authorize endpoints:

```
Script started on 2026-11-04 15:48:17+02:00 [COMMAND="hermes mcp login faxforagents" <not executed on terminal>]

  Starting OAuth flow for 'faxforagents'...
  ⚠ Server responded, but no OAuth token was obtained — authentication did not complete.

  Some providers (e.g. Google Drive, Atlassian) do not support automatic client registration. For those you must create an OAuth client yourself and add its credentials to config.yaml:

    mcp_servers:
      faxforagents:
        url: https://mcp.faxforagents.com/mcp/
        auth: oauth
        oauth:
          client_id: "<your-oauth-client-id>"
          client_secret: "<your-oauth-client-secret>"

  Then re-run `hermes mcp login faxforagents`.

Script done on 2026-11-04 15:48:20+02:00 [COMMAND_EXIT_CODE="0"]
```

This is why the manifest and the README use the sign-in URL with `?auth=required` (server release v1.8.2, 2026-11-05).

### Sign-in URL, 2026-11-04 and 2026-11-06

`hermes mcp add` with the sign-in URL started the OAuth flow at once. Its first probe counts the browser sign-in against the 30 second `connect_timeout` (NousResearch/hermes-agent#49759), so the probe timed out and the server was saved disabled:

```
Script started on 2026-11-04 17:28:53+02:00 [COMMAND="hermes mcp add faxforagents --url 'https://mcp.faxforagents.com/mcp/?auth=required' --auth oauth" <not executed on terminal>]

  Starting OAuth flow for 'faxforagents'...
  ✓ OAuth configured (tokens will be acquired on first connection)

  Connecting to 'faxforagents'...

  MCP OAuth: authorization required.
  Open this URL in your browser:

    https://api.faxforagents.com/oauth/authorize?response_type=code&client_id=https%3A%2F%2Fnousresearch.github.io%2Fhermes-agent%2Fdocs%2Foauth%2Fclient-metadata.json&redirect_uri=http%3A%2F%2F127.0.0.1%3A27890%2Fcallback&state=6KS6aLXgyrce27TqnpM87dfyia6uVlYZkMk0uPm26AE&code_challenge=TWLF_h8aaTiaOcDvUGf-xoJpLhNT2GNY8jUSJTpdpCs&code_challenge_method=S256&resource=https%3A%2F%2Fmcp.faxforagents.com%2Fmcp%2F%3Fauth%3Drequired&scope=account%3Aread+approval%3Aread+approval%3Arequest+billing%3Aread+document%3Aextract+document%3Aread+document%3Awrite+fax%3Acancel+fax%3Aquote+fax%3Aread+fax%3Asend+inbox%3Aread+inbox%3Awrite+number%3Aread+policy%3Aread+sandbox%3Awrite

  (Browser opened automatically.)

  Or paste the redirect URL here (or the ``?code=<masked>&state=...`` portion) and press Enter. Type ``skip`` + Enter to continue without this server:
  ✗ Failed to connect: Connecting to MCP server 'faxforagents' timed out after 30s (bounded by connect_timeout; an OAuth login also by oauth.timeout); CancelledError
  Check the server is running and the URL/command in its config, then run: hermes mcp test faxforagents
  Save config anyway (you can test later)? [y/N]: Y
  Pasted input did not contain ``code=`` or ``error=`` — ignoring.
Y
  ✓ Saved 'faxforagents' to config (disabled)
  Fix the issue, then: hermes mcp test faxforagents

Script done on 2026-11-04 17:38:59+02:00 [COMMAND_EXIT_CODE="0"]
```

`hermes mcp login faxforagents --flow browser` on unpatched Hermes 0.22.7. The browser completed consent, the redirect reached the loopback listener, and Hermes stalled until its 325 second budget ran out. Four runs ended this way. The paste variant below shows the same stall:

```
Script started on 2026-11-06 01:48:05+02:00 [COMMAND="hermes mcp login faxforagents --flow browser" <not executed on terminal>]

  Starting OAuth flow for 'faxforagents'...

  MCP OAuth: authorization required.
  Open this URL in your browser:

    https://api.faxforagents.com/oauth/authorize?response_type=code&client_id=https%3A%2F%2Fnousresearch.github.io%2Fhermes-agent%2Fdocs%2Foauth%2Fclient-metadata.json&redirect_uri=http%3A%2F%2F127.0.0.1%3A27890%2Fcallback&state=3XkNwf7vvyenLtd-1jBxIScF1MJcSASyKJYOmiT_zgQ&code_challenge=XZdd09PXCPLiE29ZMepNQoOQ3kE8RvNidj7h3gsCAmc&code_challenge_method=S256&resource=https%3A%2F%2Fmcp.faxforagents.com%2Fmcp%2F%3Fauth%3Drequired&scope=account%3Aread+approval%3Aread+approval%3Arequest+billing%3Aread+document%3Aextract+document%3Aread+document%3Awrite+fax%3Acancel+fax%3Aquote+fax%3Aread+fax%3Asend+inbox%3Aread+inbox%3Awrite+number%3Aread+policy%3Aread+sandbox%3Awrite

  (Browser opened automatically.)

  Or paste the redirect URL here (or the ``?code=<masked>&state=...`` portion) and press Enter. Type ``skip`` + Enter to continue without this server:
http://127.0.0.1:27890/callback?code=<masked>&state=3XkNwf7vvyenLtd-1jBxIScF1MJcSASyKJYOmiT_zgQ&iss=https%3A%2F%2Fapi.faxforagents.com
  Got authorization code from paste — completing flow.
  ✗ Authentication failed: MCP call timed out after 325.0s (configured timeout: 325.0s)

Script done on 2026-11-06 01:53:41+02:00 [COMMAND_EXIT_CODE="0"]
```

Cause: a Hermes bug, not the server. The callback listener's handler has no timeout, so an idle second browser socket parks it and the synchronous `server.shutdown()` with it. Reported with a one line fix and a regression test in NousResearch/hermes-agent#149771. Production logs confirm the code was issued and the token endpoint was never asked.

The same login path (`_reauth_oauth_server`, what `hermes mcp login` calls) with that one line applied to `tools/mcp_oauth.py`, run through a small driver that adds DEBUG logging. The idle socket was held open for 400 seconds by a browser stand-in and the login completed 6 seconds after the redirect:

```
Script started on 2026-11-06 02:23:34+02:00 [COMMAND="/home/ben/.hermes/installs/266f0c92e4ae0214/environments/6353008e0d6a429189cf32921542f427/venv/bin/python /tmp/claude-1000/-home-ben/f332b124-3794-4fa0-b1ce-f5f828f08ec6/scratchpad/hermes/repro_login.py /tmp/claude-1000/-home-ben/f332b124-3794-4fa0-b1ce-f5f828f08ec6/scratchpad/hermes/debug-9.log" <not executed on terminal>]

  Starting OAuth flow for 'faxforagents'...

  MCP OAuth: authorization required.
  Open this URL in your browser:

    https://api.faxforagents.com/oauth/authorize?response_type=code&client_id=https%3A%2F%2Fnousresearch.github.io%2Fhermes-agent%2Fdocs%2Foauth%2Fclient-metadata.json&redirect_uri=http%3A%2F%2F127.0.0.1%3A27890%2Fcallback&state=pti9UsD2FPtJKDQ1K8vqizRUsKFemi3wU8XGtCQ3wjA&code_challenge=RliBkuTZCu2fMbU07-ixT29mIcYa7rwqHfSLIbZZCfA&code_challenge_method=S256&resource=https%3A%2F%2Fmcp.faxforagents.com%2Fmcp%2F%3Fauth%3Drequired&scope=account%3Aread+approval%3Aread+approval%3Arequest+billing%3Aread+document%3Aextract+document%3Aread+document%3Awrite+fax%3Acancel+fax%3Aquote+fax%3Aread+fax%3Asend+inbox%3Aread+inbox%3Awrite+number%3Aread+policy%3Aread+sandbox%3Awrite

  (Browser opened automatically.)

  Or paste the redirect URL here (or the ``?code=<masked>&state=...`` portion) and press Enter. Type ``skip`` + Enter to continue without this server:
  ✓ Authenticated — 15 tool(s) available
RESULT True

Script done on 2026-11-06 02:23:56+02:00 [COMMAND_EXIT_CODE="0"]
```

- [x] Discovery succeeded against the exact endpoint `https://mcp.faxforagents.com/mcp/?auth=required`, trailing slash kept.
- [x] Consent host `api.faxforagents.com`. Hermes used its hosted client ID metadata document as client id, PKCE S256, redirect `http://127.0.0.1:27890/callback`, and the `iss` parameter came back on the redirect. Requested scopes are listed in the authorize URLs above and all were granted.
- [x] Consent succeeded. Token exchange completed on patched Hermes and on unpatched Hermes whenever the browser closed its idle socket within the budget.
- [x] A new process reused the stored token: `hermes mcp test` on 2026-11-06 connected in about one second without a browser.
- [ ] Refresh and revoked consent behaviour: not recorded yet.
- [ ] `get_fax_capabilities` through Hermes: not called yet.
- [x] Trust: the direct server has no `trust` setting in `config.yaml`. The portable package declares `trust: untrusted` separately.

## Tool discovery

`hermes mcp test faxforagents` on 2026-11-06, after re-enabling the saved server:

```
Script started on 2026-11-06 02:30:00+02:00 [COMMAND="hermes mcp test faxforagents" <not executed on terminal>]

  Testing 'faxforagents'...
  Transport: HTTP → https://mcp.faxforagents.com/mcp/?auth=required
  Auth: OAuth 2.0
  ✓ Connected (1063ms)
  ✓ Tools discovered: 15

    get_guide                   Read the Fax for Agents manual and tool workflow. Start...
    get_fax_capabilities        Read account limits, routes, formats, prices and creden...
    prepare_fax                 Create a fax document from text, Markdown, HTML or a co...
    get_fax_document            Read one fax document and its page previews. Use the do...
    quote_fax                   Price one prepared document for one fax destination. Us...
    send_approved_fax           Queue one quoted outbound fax for delivery. Use after q...
    get_fax_status              Read one outbound fax's delivery state and attempts. Us...
    list_faxes                  List outbound faxes your organization sent, newest firs...
    get_fax_balance             Read available and held wallet funds in the credential'...
    cancel_fax                  Request cancellation of one outbound fax. Use get_fax_s...
    request_human_review        Ask a person to approve a quoted send or help with a fa...
    get_review_status           Read the human approval decision for one review request...
    list_inbox                  List received faxes on your organization's numbers, new...
    read_inbound_fax            Read one received fax with its page count, document ref...
    extract_fax_data            Start or retrieve OCR and optional structured field ext...

Script done on 2026-11-06 02:30:02+02:00 [COMMAND_EXIT_CODE="0"]
```

```
Script started on 2026-11-06 02:35:41+02:00 [COMMAND="hermes mcp list" <not executed on terminal>]

  MCP Servers:

  Name             Transport                      Tools        Status    
  ──────────────── ────────────────────────────── ──────────── ──────────
  faxforagents     https://mcp.faxforagents....   all          ✓ enabled

Script done on 2026-11-06 02:35:42+02:00 [COMMAND_EXIT_CODE="0"]
```

- [x] All 15 discovered names match the 15 tools in `skills/fax-for-agents/SKILL.md`.
- [x] `get_fax_document` appears. The obsolete document name does not.
- [ ] `get_guide`, `get_fax_capabilities`, `get_fax_balance`, `list_faxes`, `list_inbox`, `get_fax_status`, `read_inbound_fax` through Hermes: not called yet.
- [ ] Missing scope errors: not recorded yet.

## Approval and sandbox sending

Not run through Hermes yet. The sandbox send path was proven through other hosts and the CLI, not from a Hermes session.

- [ ] `prepare_fax` and `quote_fax` for the sandbox destination `+15550000001`.
- [ ] Hermes permission prompt for write-capable tools under `trust: untrusted`.
- [ ] `request_human_review`, `get_review_status`, `send_approved_fax`, `get_fax_status`, idempotent retry, `cancel_fax`.

## Inbox and extraction

- [ ] Not run through Hermes yet.

## Release gates

- [x] Costs, network disclosure, credentials and capability descriptions reviewed in the README.
- [x] Validator run against a clean export: passed.
- [x] The validator accepts the JSON-only portable layout. The submission guide's YAML wording conflicts with the 0.22.7 loader and is noted in the README.
- [x] Published and tagged `v0.1.1` on 2026-11-06.
- [x] Catalog `sha` set to the release commit.
- [x] Catalog entries proposed through maintainer review: NousResearch/hermes-agent#148907 and #148908.
- [x] Directory suggestions opened after the public repository and this evidence existed, see `submissions/`.
