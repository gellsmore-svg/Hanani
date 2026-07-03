# Hanani — the Intelligence Synthesis Engine

**Hanani** is a geopolitical news *reasoning* platform. It synthesises evidence
from multiple reports, extracts underlying factors, generates competing
hypotheses, and preserves the full reasoning trace — asking not *"What happened?"*
but *"What do all available reports imply when combined?"*

> Named for Hanani, who brought Nehemiah intelligence from Judah about conditions
> at the wall (Nehemiah 1:2) — a witness who travelled from the conflict zone to
> report what the scattered accounts meant taken together.

The guiding question:

> **What do all available reports imply when combined?**

## Status

**v0.1 — design stage.** Philosophy, requirements, and architecture are set.
Factor taxonomy and orchestration scaffold are in place.

```bash
hanani --help              # project purpose + pointers
hanani factors             # factor taxonomy (scaffold)
hanani valhalla status     # orchestration layer (scaffold)
```

## Core principle

> Every report is a witness, not a verdict. Combined reports imply factors;
> factors support hypotheses; hypotheses compete under equal scrutiny.

## What Hanani does

An evidence-synthesis engine, not a news reader.

- **Multi-source ingestion:** news feeds, documents, structured data, OSINT metadata.
- **Claim extraction:** entities, events, assertions with provenance.
- **Evidence graph:** corroboration and conflict edges between reports.
- **Factor identification:** troop movements, logistics, sanctions, diplomatic
  signalling, satellite imagery, industrial production, doctrine, propaganda
  signals, … as explicit variables.
- **Competing hypotheses:** generated from factor combinations; debated under
  equal scrutiny.
- **Multi-LLM debate:** which reports corroborate, which conflict, which appear
  propagandistic, which assumptions drive disagreement.
- **Confidence estimates:** structural, not popularity-based; permitted uncertainty.
- **Reasoning trace:** every synthesis decision inspectable.

### Initial focus areas

- Russia–Ukraine
- Hormuz Strait / US–Iran–Gulf states

## Pipeline (target)

```
News feeds → semantic extraction → claim extraction → evidence graph
  → factor identification → competing hypotheses → multi-LLM debate
  → confidence estimates → predictions / scenario analysis
```

## Place in the family

| Sibling | Role in Hanani |
|---|---|
| [Milcah](https://github.com/gellsmore-svg/Milcah) | argument evaluation, multi-LLM debate |
| [Tirzah](https://github.com/gellsmore-svg/tirzah) | memory / retrieval over ingested reports |
| [Mahalath](https://github.com/gellsmore-svg/mahalath) | ontology / factor definitions |
| [Hoglah](https://github.com/gellsmore-svg/hoglah) | local-first LLM execution queue |
| [Galeed](https://github.com/gellsmore-svg/galeed) | process trace / reasoning telemetry |
| [Cairn](https://github.com/gellsmore-svg/Cairn) | process meta-language |
| [Keturah](https://github.com/gellsmore-svg/keturah) | LLM-consumable capability manifest |
| [Ed](https://github.com/gellsmore-svg/Ed) | scripture translation reasoning (separate project, private) |

**Valhalla** (internal orchestration codename) coordinates the multi-agent
workflow. It composes the siblings; it does not replace them.

## Develop

```bash
git clone git@github.com:gellsmore-svg/Hanani.git   # private
cd Hanani
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## Feedback

This is early. See [CONTRIBUTING.md](CONTRIBUTING.md). Security: [SECURITY.md](SECURITY.md).

## License

[Apache License 2.0](LICENSE).