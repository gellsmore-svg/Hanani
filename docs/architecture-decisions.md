# Architecture Decisions (append-only)

## ADR-001 — Project name: Hanani

**Date:** 2026-07-03

**Context:** Geopolitical news evidence synthesis, separated from the Ed scripture
translation project. Need a biblical name consistent with the family.

**Decision:** **Hanani** — the one who brought Nehemiah intelligence from Judah
about conditions in the conflict zone (Nehemiah 1:2).

**Rationale:** The project's purpose is to travel across scattered reports and
return with synthesised intelligence about what they imply together. The name is
provisional — the user did not specify a product name for the news app in the
original dictation.

---

## ADR-002 — Separate repository from Ed

**Date:** 2026-07-03

**Context:** Bible translation and news synthesis were incorrectly combined in Ed.

**Decision:** Hanani is an independent sibling repository. Ed is scripture only.

**Rationale:** Different corpora, witness types, schemas, and user goals.

---

## ADR-003 — Private repository

**Date:** 2026-07-03

**Decision:** GitHub visibility is **private**.