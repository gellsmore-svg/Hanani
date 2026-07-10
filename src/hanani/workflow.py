"""Hanani workflow orchestration — internal to this project."""

from __future__ import annotations

STATUS = "vertical-slice"


def workflow_status() -> str:
    return (
        "Hanani workflow orchestration\n"
        f"  status: {STATUS}\n"
        "  implemented: ingest → atoms → Layer 1 rhetoric → Layer 2 mechanisms → persist\n"
        "    (`hanani ingest`), Tirzah memory push (`hanani push-tirzah`), and the\n"
        "    Milcah multi-LLM debate over admissible atoms (`hanani debate`)\n"
        "  pending: evidence graph → hypotheses → synthesise → trace\n"
        "  siblings: Milcah, Tirzah, Hoglah, Galeed\n"
    )
