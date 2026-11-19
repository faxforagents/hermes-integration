# Changelog

## Unreleased

The hosted server lists 17 tools since 2026-11-12. The skill lists `request_card_payment` and `get_card_payment_status`.
The outputs in `tests/installation.md` are from 2026-11-06 and still show 15.

Pinned the stdio package to `faxforagents-mcp@0.5.9`. Its stdio server registers the same 17 tools as the hosted server.
The stdio check in `tests/installation.md` now names 0.5.9 and has still not been run.

The tests now pass on a fresh clone. `tests/fetch-hermes.sh` downloads the Hermes `v0.22.7` files they load and checks each SHA-256 pin.
The YAML fixture moved to `tests/fixtures/`, and the version check reads `plugin.json`. CI runs the fetch and all eight tests on pull requests and on `main`.

## 0.1.1 (2026-11-06)

Hosted OAuth now uses the sign-in URL `https://mcp.faxforagents.com/mcp/?auth=required`.
The plain URL answers anonymous `initialize` with 200, so Hermes 0.22.7 skipped the sign-in and `hermes mcp login` ended without a token.
The strict URL answers 401 with the OAuth metadata pointer and Hermes runs the browser sign-in.
Recorded the real Hermes 0.22.7 outputs in `tests/installation.md`: `hermes plugins validate` passed, sign-in completed, `hermes mcp test` found 15 tools.
Documented the Hermes 0.22.7 login stall (NousResearch/hermes-agent#149771) and its workaround.
Replaced the Pillow conflict note: the official installer provisions its own environment and works, a pip build does not.

## 0.1.0 (2026-11-04)

Prepared the Hermes package with hosted OAuth and portable stdio configuration.
Pinned the stdio package to `faxforagents-mcp@0.4.1`.
Added the fax workflow skill and Hermes write approval declaration.
Added draft catalog entries, submission descriptions, and an installation checklist.
Hermes CLI installation failed because upstream dependencies require conflicting Pillow versions.
OAuth consent and authenticated tool checks remain pending.
