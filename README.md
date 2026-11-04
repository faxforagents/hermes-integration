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
  <a href="https://faxforagents.com/changelog/">Changelog</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f6feb" alt="MIT licence"></a>
  <a href="skills/fax-for-agents/SKILL.md"><img src="https://img.shields.io/badge/MCP-15%20tools-6b4fbb" alt="15 MCP tools"></a>
</p>

Fax for Agents provides fax tools for [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research.
Fax for Agents is made by JSB Holdings LLC.
This package contains a workflow skill, portable MCP configuration, and hosted OAuth catalog drafts.

Version `0.1.0` is an unpublished draft.
Nothing has been submitted to a catalog.
OAuth consent and authenticated installation remain untested.
Hermes CLI installation failed because upstream dependencies require conflicting Pillow versions.
Portable discovery and loader registration pass eight isolated tests against unmodified Hermes `v0.22.7` source.
See the [build record](.coding-agent/summary.md) and [installation checklist](tests/installation.md).

## Hosted OAuth

Run these commands with your installed Hermes CLI.
Keep the endpoint's trailing slash.

```bash
hermes mcp add faxforagents --url https://mcp.faxforagents.com/mcp/ --auth oauth
hermes mcp login faxforagents
hermes mcp test faxforagents
```

Complete browser consent with your own Fax for Agents account.
Restart your Hermes session after authentication.
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
Isolated loading passes on `v0.22.7`. Full runtime compatibility remains unverified.
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

The following commands are for the planned public release.
They cannot install this unpublished repository yet.

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
Real MCP connections, secret expansion, and skill availability inside Hermes remain unchecked.

## Tools and approval

The server exposes 15 tools listed in the [workflow skill](skills/fax-for-agents/SKILL.md#hosted-tools).
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

The plugin catalog draft contains an invalid placeholder until a release commit exists.
Hermes calls that field `sha`.
The requested `commit` reminder is a comment, not a schema field.
Replace `sha` with the release's full 40-character commit before submission.
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

All eight tests passed. The [fix record](.coding-agent/summary-fix.md) links the source findings and exact output.
The full Hermes install remains blocked by Pillow `13.0.0` and browser-harness `0.1.13` requiring Pillow `12.3.0`.

Run this from the package's parent directory after installing Hermes successfully.

```bash
hermes plugins validate ./hermes-integration --install-deps
```

The command has not run for this draft.
Keep its exact output with the release evidence.
Complete [tests/installation.md](tests/installation.md) before claiming either installation path works.

## Sources and licence

The [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) documents portable loading and the trust extension.
The [catalog rules](https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/README.md) define submission fields and review requirements.
The hosted manifest follows the [Linear entry](https://github.com/NousResearch/hermes-agent/blob/main/optional-mcps/linear/manifest.yaml).
The skill adapts the [canonical Fax for Agents skill](https://github.com/faxforagents/skills/blob/main/skills/fax-for-agents/SKILL.md).

Licensed under [MIT](LICENSE).
