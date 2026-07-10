# Hanani — System Requirements

**Document:** REQ-HANANI-001  
**Version:** 0.5
**Status:** Normative — implementation shall trace to these requirements  
**Product:** Reusable geopolitical **reasoning system** (not a one-off crisis analysis tool)

---

## 1. Purpose & scope

### 1.1 Purpose

Hanani shall provide a **living, expandable reasoning engine** that:

1. Maintains **semantic graphs** of geopolitical mechanisms and rhetorical logic patterns.
2. Ingests analytical **sources** over time and decomposes them into **logic atoms**.
3. Assesses each atom **exhaustively** through layered checks (rhetoric first, mechanisms second).
4. Builds an **analysis graph** of agreements, contradictions, and gaps.
5. **Later** produces per-atom assessment summaries and a **collective narrative** with the most
   likely outcomes that fit admissible facts and tagged behavioral patterns.

### 1.2 Guiding question

> What do all available reports imply when combined?

### 1.3 In scope

- Dual semantic graphs (mechanism + rhetoric), unified store.
- Layered reasoning engine (Layer 1 → Layer 2 → record → synthesis).
- Source/witness registry, atom extraction, graph merge.
- Inspectable traces (Galeed-compatible).
- Workflow orchestration (Milcah debate, Hoglah execution).
- Human-readable **requirements and architecture published as web documentation**.

### 1.4 Out of scope (v0.x)

- Real-time news wire ingestion at scale.
- Outlet reputation scoring or prestige-weighted source ranking.
- Moral/ideological verdict engine.
- Automated military prediction marketed as certainty.

### 1.5 Core principles (shall)

| ID | Principle |
|---|---|
| P1 | **Rhetorical logic first** — structure in the text, not outlet fame |
| P2 | **Exhaustive application** — every atom gets full Layer 1 + Layer 2 treatment |
| P3 | **Living ontology** — versioned graphs; stability vs. shift recorded |
| P4 | **Reputation-blind** — training-data associations explicitly suppressed |
| P5 | **Inspectable** — every assessment step traceable |
| P6 | **Permitted uncertainty** — speculative outputs labelled |

---

## 2. Definitions

| Term | Definition |
|---|---|
| **Logic atom** | Minimal unit of assertion, causal claim, warrant, analogy, or counterfactual extracted from a source |
| **Mechanism graph** | Expandable semantic map of geopolitical analytical concepts (L1–L5 layers) |
| **Rhetoric graph** | Semantic map of fallacies, enthymemes, and audit criteria |
| **Layer 1** | Rhetorical / fallacy assessment — first truth gate |
| **Layer 2** | Mechanism tagging against the factor ontology — second assessment |
| **Admissible atom** | Atom passing Layer 1 at Strong or qualified Moderate |
| **Operational factor** | Observable variable (`troop-movements`, `sanctions`, …) linked from mechanism tags |
| **Assessment record** | Structured output per atom after Layer 1 + Layer 2 |
| **ASSSIB** | Asymmetric Sensemaking Speed & Informational Brinkmanship — cross-cutting dynamic (ontology §8.9) |
| **Speed differential** | Relative processing speed/precision/coherence between actors on a probe or signal |
| **Coherence speed profile** | Per-party trajectory of reaction speed and internal/coordination coherence inferred from source history |
| **LCD (lowest common denominator)** | Collective party constraint — effective speed/coherence bounded by slowest or least coherent member |
| **Source corpus** | Temporal article history per registered analytical source |

---

## 3. Functional requirements

### FR-GRAPH — Semantic graphs

#### FR-GRAPH-01 Mechanism graph

The system **shall** maintain an expandable **mechanism graph** containing:

- Layer 1–5 concepts (superstructure, institutional, agentic, signaling, emergent).
- Cross-cutting nodes (Schelling, Jervis, Putnam constructs).
- Historical anchor templates (e.g. Cuban Missile Crisis, Russia–Ukraine arc).
- Theatre scaffolds (Russia–Ukraine, Hormuz) as organizational hooks.
- Edges: `part_of`, `implies`, `enables`, `contradicts`, `correlates_with`, `exemplified_by`, `observed_via`.

**Acceptance:** `hanani ontology` lists ≥30 mechanism concepts; graph serialisable; version in registry.

**Status:** Seed (`hanani.ontology`, `docs/ontology/living-semantic-model.md` v0.2).

#### FR-GRAPH-01b ASSSIB cross-cutting dynamic

The mechanism graph **shall** include **Asymmetric Sensemaking Speed & Informational
Brinkmanship** (`asymmetric_sensemaking_speed_informational_brinkmanship`) as a prominent
L5 cross-cutting node with documented linkages to L2–L4 and Jervis, prospect theory, Schelling.

**Acceptance:** Ontology §8.9 present; `hanani.ontology.CROSS_CUTTING_DYNAMICS` includes ASSSIB.

**Status:** Documented v0.2.

#### FR-GRAPH-02 Rhetoric graph

The system **shall** maintain a **rhetoric graph** containing:

- Fallacy and analytical-error patterns (≥20 seed nodes).
- Enthymeme templates (load-bearing unstated assumptions).
- Audit criteria nodes (chain completeness, evidence integration, falsifiability, etc.).
- Argument roles (premise, warrant, conclusion, qualifier, rebuttal).
- Edges: `violates`, `exhibits`, `missing_warrant`, `detected_in`, `subtype_of`.

**Acceptance:** `hanani rhetoric` reports fallacy count; reputation is not an input to matching.

**Status:** Seed (`hanani.rhetoric`, `docs/ontology/rhetorical-logic-graph.md` v0.1).

#### FR-GRAPH-03 Unified graph store

The system **shall** store mechanism nodes, rhetoric nodes, logic atoms, sources, and
analysis edges in one **typed graph** with query API (neighbors, by kind).

**Acceptance:** `hanani.graph.SemanticGraph` supports add/query; atom edges include `agrees`, `contradicts`, `evaluates`, `tags`.

**Status:** Scaffold (`hanani.graph`).

#### FR-GRAPH-04 Graph expansion governance

New mechanism or rhetoric nodes **shall** be added only with documented justification
(evidence from audited atoms or cited scholarly mechanism — not outlet prestige).

**Acceptance:** Changelog entry required per expansion; version bump on material change.

**Status:** Process defined; automation not implemented.

---

### FR-REASON — Reasoning engine

#### FR-REASON-01 Layered pipeline order

For every logic atom the engine **shall** execute in order:

1. **Layer 1** — rhetorical logic assessment (rhetoric graph).
2. **Layer 2** — mechanism tagging (mechanism graph) **only if** Layer 1 admissible.
3. **Assessment record** — structured merge of Layer 1 + Layer 2.
4. *(Phase 2)* Per-atom assessment summary.
5. *(Phase 3)* Contribution to collective narrative and outcome scenarios.

**Acceptance:** `ReasoningEngine.assess_atom()` enforces order; Layer 2 skipped when Layer 1 Weak.

**Status:** Scaffold (`hanani.reasoning`).

#### FR-REASON-02 Layer 1 exhaustiveness

Layer 1 **shall** evaluate each atom against **all applicable** rhetoric patterns and audit
criteria; hits **shall** be listed explicitly (no silent drops).

Layer 1 **shall** flag content discussing or implying: sensemaking/reaction speed,
over/under-reaction to sensationalism, deliberate ambiguity, or probe-to-test-coordination.

**Acceptance:** Assessment record includes `fallacy_hits`, `enthymeme_hits`, `audit_scores`,
`robustness` tier, `sensemaking_signals` when present.

**Status:** Interface defined; matcher not implemented.

#### FR-REASON-03 Layer 2 exhaustiveness

Layer 2 **shall** tag each admissible atom against **all applicable** mechanism nodes with
step-by-step justification per tag (not default 1–2 tags).

**Acceptance:** `justifications` dict keyed by tag id; empty tag set requires explicit "no mechanism match" note.

**Status:** Interface defined; tagger not implemented.

#### FR-REASON-03b Speed differential assessment (mandatory)

For **every** logic atom Layer 2 **shall** include a `speed_differential` assessment:

- Processing speed implied for each side (`fast` / `slow` / `unknown`).
- Coherence implied for each side (`high` / `medium` / `low` / `fragmented` / `unknown`).
- Optional `side_a_party_id` / `side_b_party_id` links to coherence profiles.
- Whether a differential is exploited; probe intent (`measure_reaction_speed`,
  `measure_model_precision`, `deliberate_ambiguity`, or `none_evident`).
- If no speed signal in text — **`none_evident` required explicitly** (gap signal).

**Acceptance:** `SpeedDifferentialAssessment` on assessment record; graph edges
`processes_faster_than`, `probes_sensemaking_speed`, `creates_ambiguity_to_slow`,
`exploits_speed_differential` supported.

**Status:** Schema + scaffold (`hanani.reasoning.SpeedDifferentialAssessment` v0.3).

#### FR-REASON-03c Coherence profile linkage

When party ids are supplied on `speed_differential`, the system **shall** update
individual coherence-speed profiles from the assessment and recompute affected
collective LCD profiles.

**Acceptance:** `CoherenceRegistry.ingest_assessment()` updates trajectories;
collective `lcd_*` fields refresh after member observation.

**Status:** Scaffold (`hanani.coherence`).

#### FR-REASON-04 Admissibility gate

Atoms with Layer 1 robustness **Weak** **shall not** propagate to mechanism inference,
hypothesis generation, or collective narrative unless operator override with audit trail.

**Acceptance:** `admissible_for_inference` property; graph marks inadmissible atoms.

**Status:** Implemented in scaffold.

#### FR-REASON-05 Per-atom assessment summary (Phase 2)

The system **shall** produce a human-readable **assessment summary** per atom covering:
claim, rhetoric quality, mechanism tags, confidence, conflicts, falsification conditions.

**Acceptance:** `assessment_summary` field populated; traceable to Layer 1/2 records.

**Status:** Planned.

#### FR-REASON-06 Collective narrative & outcomes (Phase 3)

The system **shall** synthesise a **single narrative** across all admissible atoms and sources:
corroboration clusters, tensions, coverage gaps, **most likely outcomes** fitting the admissible
fact set and coherent with tagged behavioral patterns; alternative scenarios with discriminating evidence.

**Acceptance:** Output includes explicit uncertainty; cites atom ids and sources; no prestige weighting.

**Status:** Planned.

---

### FR-SOURCE — Sources & atoms

#### FR-SOURCE-01 Witness registry

The system **shall** register ingested material as witnesses with opaque id, timestamp,
provenance, and content hash — **not** prestige score.

**Status:** Design only.

#### FR-SOURCE-02 Atom extraction

The system **shall** extract logic atoms from admissible source text with types:
assertion, causal_claim, analogy, intent_assessment, counterfactual, warrant, premise.

**Acceptance:** Each atom links to `source_id`; stable `atom_id`.

**Status:** Design only.

#### FR-SOURCE-03 Source-level rhetoric gate (optional)

The system **may** run a source-level Layer 1 audit before atom extraction; weak sources
**shall** be set aside with documented reasons.

**Status:** Design only.

#### FR-SOURCE-04 Source article history

The system **shall** maintain a **temporal article history** per registered source:
opaque `source_id`, per-article `article_id`, `ingested_at`, provenance, content hash,
and linked `atom_ids`.

Operators **shall** be able to inspect the chronological sequence of articles from each
source to assess how sensemaking-speed and coherence claims evolve over time.

**Acceptance:** `SourceCorpus.history(source_id)` returns articles in time order;
`hanani sources` reports corpus summary.

**Status:** Scaffold (`hanani.sources`).

---

### FR-COHERENCE — Coherence speed profiles

#### FR-COHERENCE-01 Individual party profiles

The system **shall** maintain **coherence speed profiles** for individual parties
(states, leaders, agencies) with:

- `reaction_speed` (`fast` / `slow` / `unknown`)
- `coherence` (`high` / `medium` / `low` / `fragmented` / `unknown`)
- Observation trajectory keyed to `source_id`, `article_id`, and optional `atom_id`

Profiles **shall** be updatable from assessed atoms without outlet prestige weighting.

**Acceptance:** `CoherenceSpeedProfile.trajectory()`; `CoherenceRegistry.record_observation()`.

**Status:** Scaffold (`hanani.coherence`).

#### FR-COHERENCE-02 Collective LCD constraint

For collective parties (alliances, unions, coalitions) the system **shall** compute
**lowest-common-denominator (LCD)** effective profiles:

- `lcd_reaction_speed` — no faster than the slowest member
- `lcd_coherence` — no higher than the least coherent member
- Explicit `lcd_speed_member` and `lcd_coherence_member` binding identifiers

Collective move interpretation **shall** use LCD profiles when assessing ASSSIB probes
against alliance/coalition responses.

**Acceptance:** `compute_lcd_speed()`, `compute_lcd_coherence()`;
`CoherenceRegistry.move_context()`; `hanani coherence` CLI.

**Status:** Scaffold (`hanani.coherence`).

---

### FR-ASSSIB — Asymmetric Sensemaking Speed & Informational Brinkmanship

Permanent, high-priority augmentation. Maps to ontology §8.9–§8.11 and the normative
integration prompt. Core risk target: **dangerous mismatch** in how quickly and coherently
each side makes sense of probes — not the threatened action alone.

#### FR-ASSSIB-01 Ontology integration

The living mechanism ontology **shall** include ASSSIB
(`asymmetric_sensemaking_speed_informational_brinkmanship`) as a prominent **L5 emergent
cross-cutting dynamic** with documented linkages to L2 (two-level games, selectorate),
L3 (Jervis, prospect theory, mental simulation), L4 (cheap talk, ambiguity, probing signals),
and L1 (security dilemma under time pressure).

The ontology **shall** document: low-cost probing, stress+strategic throwaway rhetoric,
differential (not absolute) speed risk, ambiguity-as-weapon, murky sensory brinkmanship,
traffic-metaphor systemic risk, and Hanani systematic-model speed advantage.

**Acceptance:** Ontology §8.9; `hanani.ontology.CROSS_CUTTING_DYNAMICS`; historical anchors
(Cuba, Ukraine, Baltic/alliance probe template); ≥3 tagging examples.

**Status:** Implemented (ontology v0.3, §8.9–§8.11).

#### FR-ASSSIB-02 Layer 1 sensemaking signal flagging

Rhetorical logic audits and atom Layer 1 assessment **shall** explicitly flag content
discussing or implying: sensemaking/reaction speed, over/under-reaction to sensationalism,
deliberate ambiguity creation, probe-to-test-coordination, leaks, or coordination lag.

**Acceptance:** `audit.sensemaking_speed_signals` in rhetoric graph;
`RhetoricAssessment.sensemaking_signals`; keyword scaffold in `hanani.rhetoric`.

**Status:** Scaffold implemented; full matcher pending.

#### FR-ASSSIB-03 Mandatory per-atom speed-differential block

**Every** logic atom Layer 2 assessment **shall** include `speed_differential` even when
no speed signal is present — **`none_evident` required explicitly** (gap signal).

Assessment **shall** answer: fast/slow per side; probe intent; differential exploited;
coherence per side when inferable; optional party id linkage.

**Acceptance:** `SpeedDifferentialAssessment` on every `MechanismAssessment`;
`hanani.assib.ATOM_SPEED_PROMPTS`; auto-tag ASSSIB when Layer 1 sensemaking signals present.

**Status:** Schema + scaffold (`hanani.reasoning` v0.3).

#### FR-ASSSIB-04 Gap analysis speed questions

Gap analysis **shall** routinely ask the normative ASSSIB questions about relative
processing speeds, sensemaking quality, differential creation/exploitation, LCD binding
members, and per-source coherence trajectories.

**Acceptance:** `hanani.assib.GAP_ANALYSIS_QUESTIONS` exported; referenced in FR-ANALYSIS-02.

**Status:** Implemented — `hanani.gaps.analyze_gaps` / `hanani gaps` sweep the persisted corpus for explicit `none_evident` gap signals and pair findings with the normative questions.

#### FR-ASSSIB-05 Retrieval prioritization

When ASSSIB-related gaps are identified, active retrieval **shall** prioritize sources
illuminating processing-speed dynamics, reaction times, alliance coordination lag, and
how sides model each other's sensemaking speed — subject to Layer 1 filter (no prestige bypass).

**Acceptance:** `hanani.assib.RETRIEVAL_PRIORITIES`.

**Status:** Priorities surfaced automatically when gaps exist (`analyze_gaps.retrieval_priorities`); the active retrieval loop itself is pending.

#### FR-ASSSIB-06 Analysis-graph speed edges

When building or updating the analysis graph, assessed atoms **shall** be able to emit
explicit speed-differential edges:

- `processes_faster_than`
- `probes_sensemaking_speed`
- `creates_ambiguity_to_slow`
- `exploits_speed_differential`

**Acceptance:** `hanani.assib.speed_edges_from_assessment()`; edges in `GRAPH_EDGE_TYPES`.

**Status:** Scaffold implemented.

#### FR-ASSSIB-07 Readiness declaration

The system **shall** expose a machine-readable readiness check confirming speed differentials
are a **first-class analytical object** for future atom processing.

**Acceptance:** `hanani.assib.readiness()` returns `ready: true` with mandatory flags.

**Status:** Implemented.

---

### FR-ANALYSIS — Analysis graph & gaps

#### FR-ANALYSIS-01 Semantic relational mapping between logic atoms

The system **shall** map assessed atoms into an analysis graph of **typed,
auditable semantic relations**, drawn only from the registered vocabulary
(`hanani.graph.ATOM_EDGE_TYPES`: agrees, contradicts, complements, implies,
gap, supports, weakens, yields, evaluates — plus the ASSSIB speed edges of
FR-ASSSIB-06).

Normative sub-requirements:

a. **Vocabulary-closed.** A relation whose kind is not in the registered
   vocabulary **shall** be rejected — model output never invents edge types.
b. **Auditable basis.** Every relation **shall** carry its basis
   (`deterministic:<rule>` or `model`) and a confidence/score property, so
   downstream reasoning can weight or filter by provenance.
c. **Two tiers.** A deterministic floor (duplicate detection, same-article
   temporal sequence, cross-source lexical corroboration candidates) **shall**
   always run offline; an optional model tier may propose richer typed
   relations (contradicts/implies/supports/weakens), validated per (a).
d. **Gate respected.** Only Layer-1-admissible atoms participate in
   inferential relations (implies/supports/weakens); duplicates and sequence
   relations may include gated atoms for corpus hygiene.
e. **Persisted.** Relations **shall** be persisted alongside the ASSSIB speed
   edges (`graph_edges.jsonl`) and countable in the corpus summary and gap
   analysis.
f. **Family-aligned.** The mapping mirrors the family pattern (Tirzah graph
   memory nodes/edges): atom→atom edges now, exportable into Tirzah's graph
   via the existing push path later.

**Acceptance:** `hanani.relations.relate_atoms` (floor + validated model tier);
`hanani relations` CLI; `map_relations` manifest capability/MCP tool; relation
records in `graph_edges.jsonl` with basis + score.

**Status:** Implemented (floor + model tier seam); relation-aware synthesis pending.

#### FR-ANALYSIS-02 Gap analysis

The system **shall** compare covered mechanism and rhetoric nodes against the full registries
and report prioritized gaps with stated information needs.

The system **shall** routinely ask: *What do current atoms imply about relative processing
speeds or sensemaking quality between key actors? Where are differentials created or exploited?*

Gap analysis **shall** cross-check per-source article histories and party coherence
trajectories when ASSSIB tags appear — especially whether collective LCD binding members
explain observed coordination lag on current moves.

**Status:** Design only (LCD scaffold available).

#### FR-ANALYSIS-03 Active retrieval

When gaps are identified, the system **shall** recommend or retrieve additional sources
subject to the **same** Layer 1 filter (no reputation bypass).

Retrieval **shall** prioritize sources illuminating processing-speed dynamics, reaction times,
and how sides model each other's sensemaking speed when ASSSIB gaps exist.

**Status:** Design only.

---

### FR-OPS — Operational factors

#### FR-OPS-01 Factor taxonomy

The system **shall** expose an operational factor list (troops, logistics, sanctions, …).

**Status:** Implemented (`hanani.factors`).

#### FR-OPS-02 Factor ↔ mechanism linkage

Mechanism tags **shall** link to operational factors where observable (`observed_via` edge).

**Acceptance:** Assessment record `factor_links` field.

**Status:** Field defined; auto-linker not implemented.

---

### FR-WORK — Orchestration & family stack

#### FR-WORK-01 Workflow orchestration

The system **shall** coordinate ingestion → reasoning → graph → debate → synthesis via
`hanani.workflow`.

**Status:** Scaffold.

#### FR-WORK-02 Milcah debate

Competing hypotheses **shall** be debated via Milcah after graph build; structural confidence
estimates **shall** be output.

**Status:** Design only.

#### FR-WORK-03 Galeed trace

Every layer hit and assessment step **shall** be emit-able as process trace events.

**Status:** Design only.

#### FR-WORK-04 Keturah manifest

Capabilities **shall** be exposed via Keturah manifest for LLM/tool consumption.

**Status:** Scaffold (`hanani.manifest`).

---

### FR-DOCS — Documentation

#### FR-DOCS-01 Requirements publication

Requirements **shall** be maintained as normative Markdown (`docs/requirements.md`) and
published as a **readable web page** buildable from the repo.

**Acceptance:** `docs/web/index.html` renders REQ-HANANI-001; `hanani docs serve` serves locally.

**Status:** This document + web build (in progress).

#### FR-DOCS-02 Architecture publication

Architecture and reasoning-system specs **shall** be linked from the docs site.

**Acceptance:** Nav links to architecture and reasoning-system pages.

**Status:** Planned (same site).

---

## 4. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-01 | **Local-first** — LLM calls through Hoglah by default |
| NFR-02 | **Python 3.11+**, pip-installable (`pip install -e .`) |
| NFR-03 | **Traces serialisable** (JSON) and human-readable |
| NFR-04 | **Standalone** — no shared platform repo with scripture translation (Ed) |
| NFR-05 | **Private repository** until explicitly published |
| NFR-06 | **Deterministic graph IDs** — node ids stable across versions where possible |
| NFR-07 | **Test coverage** — every implemented FR has pytest acceptance test |
| NFR-08 | **Docs build** — `python scripts/build_docs.py` regenerates web site from Markdown |

---

## 5. Implementation phases (traceability)

| Phase | Requirements | Target |
|---|---|---|
| **0** | FR-DOCS-*, FR-GRAPH-01/02, P1–P6 | Requirements + graph seeds + docs site |
| **1** | FR-REASON-01–04, FR-GRAPH-03 | Real Layer 1/2 matchers |
| **2** | FR-SOURCE-*, FR-COHERENCE-*, FR-ANALYSIS-01 | Ingestion + coherence profiles + atom extraction |
| **3** | FR-REASON-05, FR-ANALYSIS-02 | Per-atom summaries + gaps |
| **4** | FR-REASON-06, FR-WORK-02 | Collective narrative + Milcah |
| **5** | FR-ANALYSIS-03, FR-GRAPH-04 | Retrieval loop + ontology automation |

---

## 6. Requirement status summary

| Area | Implemented | Scaffold | Planned |
|---|---|---|---|
| Mechanism graph | — | ✓ | expand |
| Rhetoric graph | — | ✓ | expand |
| Reasoning engine | gate | ✓ | matchers |
| ASSSIB augmentation | ontology + schema | workflow constants + edges | matchers + retrieval |
| Sources / atoms | — | history scaffold | ✓ |
| Coherence profiles | — | ✓ | LCD + moves |
| Synthesis | — | — | ✓ |
| Web requirements | — | in progress | ✓ |

---

## 7. References

- [`reasoning-system.md`](reasoning-system.md) — architecture
- [`architecture.md`](architecture.md) — component diagram
- [`ontology/living-semantic-model.md`](ontology/living-semantic-model.md) — mechanism graph
- [`ontology/rhetorical-logic-graph.md`](ontology/rhetorical-logic-graph.md) — rhetoric graph
- [`vision.md`](vision.md) — product vision

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-07-05 | Initial FR1–FR9 scaffold |
| 0.2 | 2026-07-05 | Full reasoning-system requirements; dual graphs; layered engine; web docs FR |
| 0.3 | 2026-07-05 | ASSSIB dynamic; mandatory speed_differential per atom; workflow/gap/retrieval rules |
| 0.4 | 2026-07-10 | Source article history; individual/collective coherence profiles; LCD constraint; move-context hooks |
| 0.6 | 2026-07-10 | FR-ANALYSIS-01 refined into normative semantic relational mapping between logic atoms (vocabulary-closed, auditable basis, two tiers, gate-respecting, persisted); `hanani.relations` |
| 0.5 | 2026-07-10 | FR-ASSSIB-01–07 formal traceability; `hanani.assib` module; augmentation prompt mapped to normative FRs |