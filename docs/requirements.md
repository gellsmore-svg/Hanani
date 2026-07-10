# Requirements — Intelligence Synthesis Engine v0.1

Status: **specified, not yet implemented** unless marked otherwise.

---

## FR1 — Report / Witness Registry

- Ingest reports with source, timestamp, bias classification, provenance.
- Support structured data attachments and OSINT metadata.

**Status:** design only.

## FR2 — Dual Semantic Graphs

- **Mechanism graph:** expandable L1–L5 concepts, historical anchors, theatre scaffolds.
- **Rhetoric graph:** fallacies, enthymemes, audit criteria — Layer 1 truth assessment.
- Unified store with typed nodes/edges; versioned Markdown + machine registry.

**Status:** seed (`hanani.ontology`, `hanani.rhetoric`, `hanani.graph`).

## FR2b — Factor Taxonomy (operational observables)

- Define geopolitical factors as data; link **from** mechanism tags.

**Status:** scaffold (`hanani.factors`).

## FR2c — Reasoning Engine

- Per-atom pipeline: Layer 1 rhetoric → Layer 2 mechanisms → assessment record.
- Later: per-atom summary, collective narrative, likely outcomes.

**Status:** scaffold (`hanani.reasoning`). Spec: [`reasoning-system.md`](reasoning-system.md).

## FR3 — Workflow Orchestration

- Coordinate ingestion → graph → debate → synthesis via `hanani.workflow`.
- Schedule Milcah for multi-LLM debate; emit telemetry via Galeed.

**Status:** scaffold (`hanani.workflow`).

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