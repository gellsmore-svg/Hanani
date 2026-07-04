# Architecture Decisions (append-only)

## ADR-001 — Project name: Hanani

**Date:** 2026-07-03

**Context:** Geopolitical news evidence synthesis — a standalone project, not linked
to scripture translation or any shared platform repo.

**Decision:** **Hanani** — the one who brought Nehemiah intelligence from Judah
about conditions in the conflict zone (Nehemiah 1:2).

**Rationale:** The project's purpose is to travel across scattered reports and
return with synthesised intelligence about what they imply together. The name is
provisional — the user did not specify a product name for the news app in the
original dictation.

---

## ADR-002 — Fully independent from Ed and any shared platform

**Date:** 2026-07-03 (revised)

**Context:** An interim shared-platform repo incorrectly linked Hanani to Ed.

**Decision:** Hanani is fully standalone. Internal orchestration is
`hanani.workflow`. No dependency on Ed or scripture translation.

**Rationale:** Different corpora, witness types, schemas, and user goals.

---

## ADR-003 — Private repository

**Date:** 2026-07-03

**Decision:** GitHub visibility is **private**.