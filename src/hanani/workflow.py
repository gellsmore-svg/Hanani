"""Hanani workflow orchestration — internal to this project."""

from __future__ import annotations

STATUS = "vertical-slice"


def workflow_status() -> str:
    return (
        "Hanani workflow orchestration\n"
        f"  status: {STATUS}\n"
        "  implemented: ingest → atoms → Layer 1 rhetoric → Layer 2 mechanisms → persist\n"
        "    (`hanani ingest` — deterministic floor + optional Hoglah model tier)\n"
        "  pending: evidence graph → hypotheses → multi-LLM debate → synthesise → trace\n"
        "  siblings: Milcah, Tirzah, Hoglah, Galeed\n"
    )
