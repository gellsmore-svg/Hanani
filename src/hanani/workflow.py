"""Hanani workflow orchestration — internal to this project."""

from __future__ import annotations

from hanani.assib import GAP_ANALYSIS_QUESTIONS, RETRIEVAL_PRIORITIES, readiness

STATUS = "vertical-slice"


def workflow_status() -> str:
    asssib = readiness()
    return (
        "Hanani workflow orchestration\n"
        f"  status: {STATUS}\n"
        "  implemented: ingest → atoms → Layer 1 rhetoric → Layer 2 mechanisms → persist\n"
        "    (`hanani ingest`), Tirzah memory push (`hanani push-tirzah`), and the\n"
        "    Milcah multi-LLM debate over admissible atoms (`hanani debate`)\n"
        f"  ASSSIB: {asssib['dynamic']} — speed_differential mandatory per atom\n"
        f"  gap questions: {len(GAP_ANALYSIS_QUESTIONS)} normative prompts\n"
        f"  retrieval priorities: {len(RETRIEVAL_PRIORITIES)} when ASSSIB gaps exist\n"
        "  pending: evidence graph → hypotheses → synthesise → trace\n"
        "  siblings: Milcah, Tirzah, Hoglah, Galeed\n"
    )
