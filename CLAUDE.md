# CLAUDE.md — Hanani handoff note

Context for Claude (or any agent) picking up work in this repo.

**Repo:** `/home/cello/domains/Hanani` · GitHub `gellsmore-svg/Hanani`  
**Product:** Standalone geopolitical **reasoning system** — dual semantic graphs + layered atom assessment. Not Ed/Bible, not a one-off crisis briefing.

**Guiding question:** *What do all available reports imply when combined?*

---

## What's new (read this first)

Recent work added three major layers on top of the original dual-graph scaffold:

### 1. ASSSIB — Asymmetric Sensemaking Speed & Informational Brinkmanship

Permanent cross-cutting dynamic. Core insight: the risk is often a **mismatch in sensemaking speed/coherence**, not the threatened action itself.

| Artifact | Location |
|---|---|
| Ontology definition + examples | `docs/ontology/living-semantic-model.md` **§8.9–§8.11** |
| Normative FRs | `docs/requirements.md` **FR-ASSSIB-01–07** (REQ v**0.5**) |
| Code hooks | `src/hanani/assib.py` |
| Per-atom schema | `SpeedDifferentialAssessment` in `src/hanani/reasoning/__init__.py` |
| CLI readiness | `hanani asssib` |

Every atom **must** carry `speed_differential` (use `none_evident` explicitly when absent). Layer 1 flags `sensemaking_signals`; Layer 2 auto-tags ASSSIB when signals present.

### 2. Coherence speed profiles + collective LCD

Reaction **speed** alone is insufficient for alliances. Hanani also tracks **coherence** and computes **lowest-common-denominator (LCD)** constraints for collective actors.

| Artifact | Location |
|---|---|
| Requirements | `docs/requirements.md` **FR-COHERENCE-01/02**, **FR-REASON-03c** |
| Ontology | `docs/ontology/living-semantic-model.md` **§8.9b** |
| Code | `src/hanani/coherence.py` — `CoherenceRegistry`, `compute_lcd_speed/coherence`, `move_context()` |
| CLI | `hanani coherence` |

### 3. Source article history

Per-source temporal witness corpus (reputation-blind).

| Artifact | Location |
|---|---|
| Requirements | `docs/requirements.md` **FR-SOURCE-04** |
| Code | `src/hanani/sources.py` — `SourceCorpus.history(source_id)` |
| CLI | `hanani sources` |

### 4. Executable vertical slice (first real pipeline)

Previously schema-only; now runnable end-to-end on one article:

```
ingest → extract atoms → Layer 1 rhetoric → Layer 2 mechanisms → persist
```

| Artifact | Location |
|---|---|
| Pipeline | `src/hanani/pipeline.py` — `ingest_article()` |
| Persistence | `src/hanani/store.py` — JSONL under `~/.hanani/` |
| CLI | `hanani ingest`, `hanani corpus` |
| ASSSIB edges in pipeline | `speed_edges_from_assessment()` persisted to `graph_edges.jsonl` (FR-ASSSIB-06) |

Optional model tier via Hoglah (`--hoglah-model`); deterministic floor always runs offline.

### 5. Family stack integrations

| Feature | Module | CLI |
|---|---|---|
| Tirzah memory push | `src/hanani/tirzah_push.py` | `hanani push-tirzah` |
| Milcah multi-LLM debate | `src/hanani/debate.py` | `hanani debate` |
| Keturah manifest + MCP | `src/hanani/manifest.py`, `mcp_handlers.py` | — |

---

## Version pins (current)

| Component | Version |
|---|---|
| Requirements (REQ-HANANI-001) | **0.5** |
| Mechanism ontology | **0.3** (`ONTOLOGY_VERSION`) |
| Reasoning engine schema | **0.3** (`REASONING_VERSION`) |
| Rhetoric graph | **0.2** (adds `audit.sensemaking_speed_signals`) |

---

## Documentation map

| Need | File | Web (`hanani docs serve` → :8805) |
|---|---|---|
| All normative FRs | `docs/requirements.md` | `docs/web/index.html` |
| ASSSIB analytical substance | `docs/ontology/living-semantic-model.md` §8.9+ | `docs/web/ontology.html` |
| Layer 1 rhetoric graph | `docs/ontology/rhetorical-logic-graph.md` | (linked from index) |
| Pipeline architecture | `docs/reasoning-system.md` | `docs/web/reasoning-system.html` |

Build docs: `python scripts/build_docs.py` or `hanani docs build`.

---

## Key modules

```
src/hanani/
  ontology/      # L1–L5 mechanism tags, ASSSIB, COHERENCE_LEVELS, SPEED_GRAPH_EDGES
  rhetoric/      # fallacies, SENSEMAKING_SIGNAL_KEYWORDS, audit criteria
  reasoning/     # ReasoningEngine, SpeedDifferentialAssessment, assess_atom()
  graph/         # SemanticGraph scaffold
  sources/       # SourceCorpus, WitnessArticle, article history
  coherence/     # CoherenceRegistry, LCD, move_context()
  assib/         # GAP_ANALYSIS_QUESTIONS, RETRIEVAL_PRIORITIES, speed_edges, readiness()
  pipeline/      # ingest_article(), extract_atoms(), detect_rhetoric_hits()
  store/         # SliceStore JSONL persistence
  debate/        # Milcah debate over admissible atoms
  tirzah_push/   # push slice → Tirzah graph memory
```

---

## CLI quick reference

```bash
hanani asssib          # ASSSIB readiness (mandatory speed_differential, LCD, etc.)
hanani reasoning       # engine status
hanani ontology        # mechanism graph layers
hanani rhetoric        # fallacy count
hanani sources         # in-memory corpus summary (ingest uses SourceCorpus internally)
hanani coherence       # LCD registry summary
hanani workflow status # includes ASSSIB gap-question count

hanani ingest article.txt --source-id SRC --title "..."
hanani corpus          # ~/.hanani summary
hanani push-tirzah     # optional [tirzah] extra
hanani debate          # optional [milcah] extra
hanani docs serve      # http://127.0.0.1:8805
```

---

## Implemented vs scaffold vs planned

| Area | Status |
|---|---|
| Dual graph seeds (mechanism + rhetoric) | Scaffold ✓ |
| Layer 1/2 matchers (exhaustive) | Scaffold — pipeline has deterministic cue rules + optional Hoglah |
| ASSSIB ontology + FR traceability | **Implemented** (docs + schema + assib module) |
| Mandatory speed_differential per atom | **Implemented** (schema; pipeline always emits block) |
| Speed edges in pipeline | **Implemented** (FR-ASSSIB-06 wired in `pipeline.py`) |
| Coherence profiles + LCD | Scaffold (`coherence.py`; not auto-wired in ingest yet) |
| Source article history | Scaffold in `sources.py`; wired in `pipeline.ingest_article()` |
| Gap analysis runner | Constants only (`GAP_ANALYSIS_QUESTIONS`) |
| Active retrieval loop | Constants only (`RETRIEVAL_PRIORITIES`) |
| Per-atom summaries (Phase 2) | Planned |
| Collective narrative (Phase 3) | Planned |

**58 tests passing** (`pytest`). CI: ruff + pytest.

---

## Sensible next steps

1. **Wire coherence into ingest** — call `CoherenceRegistry.ingest_assessment()` when `speed_differential` has party ids.
2. **Auto-infer speed/coherence** from probe/leak/coordination-lag language in atoms (extend deterministic floor or Hoglah prompt).
3. **Gap analysis command** — `hanani gaps` running `GAP_ANALYSIS_QUESTIONS` over `~/.hanani` assessments.
4. **First live source cycle** — ingest real analytical text; review ASSSIB tags + LCD on a collective (NATO/EU).
5. **Phase 2** — populate `assessment_summary` per atom.

---

## Recent commits (newest first)

```
08faced feat: wire FR-ASSSIB-06 speed edges into the executable pipeline
c8fa28a Formalize ASSSIB augmentation as FR-ASSSIB-01–07 requirements
afbe169 Add source history and coherence-speed profiles with collective LCD
8b72d37 feat: integrate ASSSIB sensemaking-speed dynamic (ontology v0.2, req v0.3)
eb504e0 feat: vertical slice — ingest → atoms → Layer 1 → Layer 2 → persist
```

---

## Principles (do not violate)

- **Rhetoric first** — Layer 1 before Layer 2; Weak atoms do not propagate.
- **Reputation-blind** — no outlet prestige weighting anywhere.
- **Inspectable** — JSONL store, traceable assessment records.
- **Standalone** — no shared repo with Ed/scripture work.

---

*Last updated: 2026-07-10 — after ASSSIB formalization + pipeline speed-edge wiring.*