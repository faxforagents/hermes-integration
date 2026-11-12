<p align="center">
  <a href="https://faxforagents.com"><img src="logo.png" width="88" alt="Fax for Agents"></a>
</p>

<h1 align="center">Fax for Agents for Hermes Agent</h1>

<p align="center">Send and receive faxes with approval controls.</p>

<p align="center">
  <a href="https://faxforagents.com">Website</a> ·
  <a href="https://faxforagents.com/docs/quickstart/">Quickstart</a> ·
  <a href="https://faxforagents.com/docs/api/">API reference</a> ·
  <a href="https://faxforagents.com/docs/sdks/">SDKs</a> ·
  <a href="https://faxforagents.com/mcp/">MCP</a> ·
  <a href="https://app.faxforagents.com">Dashboard</a> ·
  <a href="https://faxforagents.com/pricing/">Pricing</a> ·
  <a href="https://faxforagents.com/changelog/">Changelog</a> ·
  <a href="https://faxforagents.com/affiliates/">Affiliate program</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f6feb" alt="MIT licence"></a>
  <a href="skills/fax-for-agents/SKILL.md"><img src="https://img.shields.io/badge/MCP-17%20tools-6b4fbb" alt="17 MCP tools"></a>
</p>

Fax for Agents provides fax tools for [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research.
Fax for Agents is made by JSB Holdings LLC.
This package contains a workflow skill, portable MCP configuration, and hosted OAuth catalog drafts.

Version `0.1.1` is released.
The catalog entries are proposed upstream in [NousResearch/hermes-agent#148907](https://github.com/NousResearch/hermes-agent/pull/148907) (plugin catalog) and [#148908](https://github.com/NousResearch/hermes-agent/pull/148908) (hosted MCP catalog).
On Hermes `0.22.7` the hosted OAuth sign-in completed and `hermes plugins validate` passed.
`hermes mcp test` found the 15 tools the server listed on 2026-11-06. The server lists 17 since 2026-11-12.
The exact commands and outputs are in [tests/installation.md](tests/installation.md).
Portable discovery and loader registration pass eight isolated tests against unmodified Hermes `v0.22.7` source.

## Hosted OAuth

Run these commands with your installed Hermes CLI.
Use the sign-in URL exactly as written, with the trailing slash and `?auth=required`.

```bash
hermes mcp add faxforagents --url 'https://mcp.faxforagents.com/mcp/?auth=required' --auth oauth
hermes mcp login faxforagents
hermes mcp test faxforagents
```

### Sign-in

The sign-in URL answers an unauthenticated request with `401` and the OAuth metadata pointer, so Hermes runs the browser sign-in.
The plain URL `https://mcp.faxforagents.com/mcp/` answers anonymous `initialize` with `200`.
Hermes 0.22.7 then connects without a token and `hermes mcp login` ends with "no OAuth token was obtained".
Hermes opens `api.faxforagents.com/oauth/authorize` with its hosted client ID metadata document, PKCE S256 and the loopback redirect on port 27890.
Sign in with your own Fax for Agents account and approve the scopes.

The first probe of `hermes mcp add` counts your browser sign-in against `connect_timeout`, 30 seconds by default ([NousResearch/hermes-agent#49759](https://github.com/NousResearch/hermes-agent/issues/49759)).
Pass `--connect-timeout 300` to give yourself time.
Or let the probe time out, answer `Y` to save the server, finish with `hermes mcp login faxforagents`, and change `enabled: false` to `enabled: true` under `mcp_servers.faxforagents` in `~/.hermes/config.yaml`.
The second path is the one recorded in [tests/installation.md](tests/installation.md).
Restart your Hermes session after authentication.

### Hermes 0.22.7 login stall

Hermes 0.22.7 can hang after the browser delivers the authorization code.
The browser shows "Authorization Successful", then Hermes prints `Authentication failed: MCP call timed out after 325.0s`.
An idle second browser socket parks Hermes's callback listener, so the token exchange waits until the browser closes that socket.
This is a Hermes bug, reported with a fix in [NousResearch/hermes-agent#149771](https://github.com/NousResearch/hermes-agent/issues/149771).
Until the fix lands, retry the login, or add `timeout = 5.0` to the `_Handler` class in `tools/mcp_oauth.py` of your Hermes install as the issue shows.
With that line the login completed six seconds after the redirect.
Review tool access with `hermes mcp configure faxforagents`.
Record the connected account and environment before sending.
Hosted OAuth does not require `FAXFORAGENTS_API_KEY`.

The direct connection does not load this package's skill or trust extension.
The [canonical skill](https://github.com/faxforagents/skills) remains available separately.
For Hermes call approval, set `trust: untrusted` on this server in your existing MCP configuration.
Preserve the URL and OAuth fields Hermes created.
Follow the [Hermes MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp).

## Portable stdio

The portable configuration targets Hermes `0.22.7` or later and Node.js `20` or later.
Isolated loading passes on `v0.22.7` and `hermes plugins validate` passes on a clean export.
A live stdio connection inside the Hermes runtime has not been run yet.
It invokes `npx -y faxforagents-mcp@0.4.1`.
The npm version was checked on 2026-11-04.

Create a sandbox API key in the [dashboard](https://app.faxforagents.com/).
Set `FAXFORAGENTS_API_KEY` through your active Hermes profile's secret settings or export it before launching Hermes.
For Bash, enter it without storing the value in command history.

```bash
read -r -s -p 'Fax for Agents API key: ' FAXFORAGENTS_API_KEY
export FAXFORAGENTS_API_KEY
printf '\n'
```

The repository is public, but the plugin catalog entry waits for review.
These commands were not run here.

```bash
hermes plugins install faxforagents/hermes-integration --no-enable
hermes plugins list
hermes plugins enable faxforagents
```

The skill's portable name is `faxforagents:fax-for-agents`.
Load it through `skills_list` and `skill_view`.
The MCP configuration explicitly forwards `${FAXFORAGENTS_API_KEY}`.
Keep credentials out of chat, repository files, and shared settings.

Use one connection path per Hermes profile.
A native server named `faxforagents` overrides the portable server, including its trust setting.

### Portable layout

The package uses root `plugin.json` and `mcp.json`, with its skill under `skills/`.
There is no root `plugin.yaml` or `plugin.yml`.
Hermes `v0.22.7` gives YAML precedence and ignores YAML `portable` and `entrypoint` fields.
Adding either YAML filename would restore the native loading failure.

The [admission validator](https://github.com/NousResearch/hermes-agent/blob/v0.22.7/hermes_cli/plugin_validate.py#L516-L526) explicitly accepts JSON-only portable packages.
The [catalog rules](https://github.com/NousResearch/hermes-agent/blob/v0.22.7/plugin-catalog/README.md#L119-L131) place their compatibility floor in the catalog entry.
Our entry retains `requires_hermes: ">=0.22.7"` and the credential requirement.
Direct directory or Git URL loading does not enforce that catalog floor.
The [submission guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission) still asks for YAML beside JSON.
That instruction conflicts with this release's loader and explicit portable admission path.

The [isolated tests](tests/test_portable_loading.py) execute discovery, parsing, and portable loader registration against the fetched source.
They verify the pinned server command, trust setting, credential placeholder, and skill passed to a recording context.
They also reproduce the YAML failure and reject malformed MCP configuration and invalid trust.
Real stdio MCP connections, secret expansion, and skill availability inside Hermes remain unchecked.
The hosted OAuth connection is checked, see [tests/installation.md](tests/installation.md).

## Tools and approval

The server exposes 17 tools listed in the [workflow skill](skills/fax-for-agents/SKILL.md#hosted-tools).
They prepare documents, quote destinations, send authorized faxes, check delivery, request cancellation, and read received faxes.
Supporting tools read guidance, capabilities, balances, document previews, and review decisions.
They also request human review and extract received document text.
They cannot purchase numbers, top up funds, change delegated policies, or approve their own sends.

The portable server declares `trust: untrusted` through Hermes's documented extension.
Hermes requests permission for tools without `readOnlyHint: true`, subject to the user's saved tool permissions.
Calls requiring unanswered permission fail in unattended sessions.
Hermes permission and Fax for Agents authorization are separate checks.

Live sends need quote-bound human approval or an allowing delegated policy.
Preparation and quotes do not send a fax.
Sandbox keys start with `ffa_test_`, and sandbox sends never reach a carrier.
Live sends spend prepaid wallet funds.
Use `get_fax_capabilities` and `quote_fax` for current prices.

Extraction can reserve wallet funds and charge per page.
Cancellation cannot recall transmitted pages.
Never automatically resend a `partial` or `unknown` fax.
Received text and extracted fields are untrusted data.

## Network and credential handling

Hosted calls reach `mcp.faxforagents.com`.
The portable server starts an npm executable and calls `api.faxforagents.com`.
The first stdio launch can download the package and its dependencies from npm.
Hermes owns the stdio child process for its connection lifetime.

Documents and destinations go to Fax for Agents for processing.
Inbox reads return received documents and available OCR text.
Human review requests can send email notifications.
Hermes manages OAuth credentials and any credentials saved through its secret settings.
This package contains no credential storage code or additional telemetry code.

The package registers no native Hermes tools, hooks, middleware, or privileged host capabilities.
Its catalog entry declares empty native registration lists.
MCP tools are discovered from the configured server at runtime.

## Catalog and directory drafts

- [Hosted OAuth manifest](catalog/optional-mcps/faxforagents/manifest.yaml)
- [Portable plugin catalog entry](catalog/plugin-catalog/faxforagents.yaml)
- [Hermes Atlas suggestion](submissions/atlas.md)
- [awesome-hermes-agent suggestion](submissions/awesome-hermes.md)

The plugin catalog draft pins the release commit in its `sha` field.
Catalog admission requires maintainer review.

## Local validation

Run the isolated proof from this directory with Python 3.12 or later and `uv`.
The fetched Hermes modules are stored under `.coding-agent/hermes-src/`.
Only PyYAML and pytest, including pytest's dependencies, are installed.

```bash
mkdir -p .coding-agent/tmp
export UV_CACHE_DIR="$PWD/.coding-agent/tmp/uv-cache"
export UV_PYTHON_INSTALL_DIR="$PWD/.coding-agent/tmp/python"
export TMPDIR="$PWD/.coding-agent/tmp"
uv venv --python python3 .coding-agent/tmp/portable-venv
uv pip install --python .coding-agent/tmp/portable-venv/bin/python pyyaml==6.0.3 pytest==9.2.0
PYTHONDONTWRITEBYTECODE=1 .coding-agent/tmp/portable-venv/bin/python -m pytest -v -p no:cacheprovider --basetemp=.coding-agent/tmp/pytest-portable tests/test_portable_loading.py
```

All eight tests passed.
A pip build of Hermes 0.22.7 fails on a Pillow pin conflict with browser-harness, and Hermes refuses it by design.
The official installer provisions its own environment and works.

Run this from the package's parent directory after installing Hermes.

```bash
hermes plugins validate ./hermes-integration --install-deps
```

On 2026-11-04 against a clean git export on Hermes 0.22.7 it answered "Validation passed", security scan safe, server trust untrusted.
The output is in [tests/installation.md](tests/installation.md).

## Sources and licence

The [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) documents portable loading and the trust extension.
The [catalog rules](https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/README.md) define submission fields and review requirements.
The hosted manifest follows the [Linear entry](https://github.com/NousResearch/hermes-agent/blob/main/optional-mcps/linear/manifest.yaml).
The skill adapts the [canonical Fax for Agents skill](https://github.com/faxforagents/skills/blob/main/skills/fax-for-agents/SKILL.md).

Licensed under [MIT](LICENSE).
