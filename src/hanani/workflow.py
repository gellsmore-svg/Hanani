"""Hanani workflow orchestration — internal to this project."""

from __future__ import annotations

STATUS = "scaffold"


def workflow_status() -> str:
    return (
        "Hanani workflow orchestration\n"
        f"  status: {STATUS}\n"
        "  pipeline: ingest → extract claims → evidence graph → factors\n"
        "    → hypotheses → multi-LLM debate → synthesise → trace\n"
        "  siblings: Milcah, Tirzah, Hoglah, Galeed\n"
    )