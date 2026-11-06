# awesome-hermes-agent submission

Filed 2026-11-06: https://github.com/0xNyk/awesome-hermes-agent/issues/576

Form: [Resource submission](https://github.com/0xNyk/awesome-hermes-agent/issues/new?template=resource-submission.yml).
The [contribution rules](https://github.com/0xNyk/awesome-hermes-agent/blob/main/CONTRIBUTING.md) require an issue, not a PR. Maintainers add accepted entries in batch commits and assign the maturity label.

## Resource details

- Name: Fax for Agents for Hermes Agent
- URL: https://github.com/faxforagents/hermes-integration
- Author: faxforagents
- Category: Integrations & Bridges
- Licence: MIT
- Suggested maturity: beta
- Disclosures ticked: affiliated with the project, depends on a paid service

## Text as filed

Brief description: Fax tools for Hermes Agent. The hosted MCP server signs in with OAuth through `hermes mcp add` and `hermes mcp login`. It exposes 15 tools. They prepare and quote a document, send after a human approval, read delivery status and evidence, and cancel. They also read the inbox and extract text from received faxes. The repository also holds a portable stdio plugin pinned to `faxforagents-mcp@0.4.1` with the Hermes `trust: untrusted` declaration, so Hermes asks before every write-capable call. A workflow skill covers approvals, delegated policies, untrusted received text and ambiguous delivery outcomes.

Why it's awesome: It is the only fax route for Hermes we know of, and it is built for an agent. A send cannot happen without a quote-bound approval or an allowing policy. The agent prepares and prices the fax, a human decides. Received faxes come back as data with OCR text, and the skill tells the agent to treat embedded instructions as data. Tested on Hermes 0.22.7 on 2026-11-06: sign-in, 15 tools discovered, `hermes plugins validate` passed, with the exact outputs in `tests/installation.md`. Nothing else on the list covers faxing.

Why now: Clinics, courts, banks and many suppliers still take documents by fax. Hermes users can now send and receive them from a session, with an approval step.

We build Fax for Agents (https://faxforagents.com). Every account starts in a free sandbox, and a live send is prepaid.
