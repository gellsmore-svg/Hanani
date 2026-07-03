# Security Policy

Hanani is an early local-first research prototype. Treat it as unsuitable for
untrusted network exposure until authentication, authorization, and data-handling
boundaries are explicitly designed and tested.

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report privately via GitHub's
[private vulnerability reporting](https://github.com/gellsmore-svg/Hanani/security/advisories/new).

Hanani ingests news feeds and external reports and orchestrates LLM calls through
Hoglah. Keep API keys and connection strings in local config and scrub them from
traces before sharing.