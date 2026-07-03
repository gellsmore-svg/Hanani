# Requirements — Intelligence Synthesis Engine v0.1

Status: **specified, not yet implemented** unless marked otherwise.

---

## FR1 — Report / Witness Registry

- Ingest reports with source, timestamp, bias classification, provenance.
- Support structured data attachments and OSINT metadata.

**Status:** design only.

## FR2 — Factor Taxonomy

- Define geopolitical factors as data (YAML/JSON schema).
- Apply factor-extraction policies per theatre / topic.

**Status:** scaffold (`hanani.factors`).

## FR3 — Valhalla Orchestration

- Coordinate ingestion → extraction → graph → debate → synthesis → trace.
- Emit telemetry via Galeed.

**Status:** scaffold (`hanani.valhalla`).

## FR4 — Claim Extraction

- Extract entities, events, assertions from ingested reports.
- Preserve source linkage and confidence state per claim.

**Status:** design only.

## FR5 — Evidence Graph

- Build graph with corroboration and conflict edges.
- Support temporal ordering and source-bias annotations.

**Status:** design only.

## FR6 — Hypothesis Generation & Debate

- Generate competing hypotheses from factor combinations.
- Multi-LLM debate (via Milcah/Hoglah) on corroboration, conflict, propaganda.
- Output structural confidence estimates.

**Status:** design only.

## FR7 — Scenario Analysis

- Predictions and scenario notes from synthesised hypotheses.
- Explicit uncertainty labelling.

**Status:** design only.

## FR8 — Reasoning Trace API

- Query: "Why was this conclusion reached?"
- Return: reports cited, factors, debate transcript, rejected hypotheses.

**Status:** design only.

## FR9 — Keturah Manifest

- Expose `capabilities()` for LLM-consumable interfaces.

**Status:** scaffold (`hanani.manifest`).

---

## Non-Functional Requirements

- **NFR1:** Local-first; LLM calls through Hoglah by default.
- **NFR2:** Python 3.11+, pip-installable.
- **NFR3:** Traces serialisable (JSON) and human-readable.
- **NFR4:** Permitted uncertainty — speculative outputs labelled.
- **NFR5:** Private repository.