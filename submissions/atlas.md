# Hermes Atlas suggestion

Filed 2026-11-06: https://github.com/ksimback/hermes-ecosystem/issues/1369

Form: [Suggest a Repo](https://github.com/ksimback/hermes-ecosystem/issues/new?template=suggest-repo.yml), following the [contribution guide](https://github.com/ksimback/hermes-ecosystem/blob/main/CONTRIBUTING.md).
Atlas automation fetches the repository metadata, runs a basic security check and generates a PR for maintainer review.

## Repository details

- Name: Fax for Agents for Hermes Agent
- Repository: https://github.com/faxforagents/hermes-integration
- Owner: faxforagents
- Category: Integrations & Bridges
- Licence: MIT

## Text as filed

Fax for Agents gives Hermes Agent fax tools. An agent can prepare and quote a document, send it after a human approval, read delivery status, cancel, and read received faxes. The repository holds the hosted OAuth setup for Hermes (`hermes mcp add`, `hermes mcp login`, `hermes mcp test`). It also holds a portable stdio plugin pinned to `faxforagents-mcp@0.4.1` with the Hermes `trust: untrusted` declaration, and a workflow skill. The catalog entries are proposed upstream in NousResearch/hermes-agent#148907 and #148908.

Tested on Hermes 0.22.7 on 2026-11-06: OAuth sign-in completed, 15 tools discovered, `hermes plugins validate` passed. The exact command outputs are in `tests/installation.md`. Every account starts in a free sandbox. A live send is prepaid and needs a quote-bound approval, which the skill documents.

We build Fax for Agents (https://faxforagents.com). MIT licence.

## Criteria check

Created after July 22, 2025: yes (2026-11-04). Stars: none yet at filing, Atlas normally wants one. Activity: released v0.1.1 on 2026-11-06.
