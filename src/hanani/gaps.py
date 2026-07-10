"""Automated ASSSIB gap analysis over the persisted corpus (FR-ASSSIB-04/05).

The pipeline records ``none_evident`` speed blocks *as explicit gap signals*
(FR-ASSSIB-03); this runner consumes them. It sweeps the stored assessments,
counts where speed/coherence evidence is missing or half-present, pairs each
finding with the normative :data:`hanani.assib.GAP_ANALYSIS_QUESTIONS`, and —
when ASSSIB gaps exist — surfaces :data:`hanani.assib.RETRIEVAL_PRIORITIES`
(the FR-ASSSIB-05 hook: what to go and read next, subject to the Layer-1
filter, no prestige bypass).

Deterministic and offline: it reads the JSONL store only.
"""

from __future__ import annotations

from typing import Any

from hanani.assib import GAP_ANALYSIS_QUESTIONS, RETRIEVAL_PRIORITIES
from hanani.ontology import SPEED_GRAPH_EDGES
from hanani.store import SliceStore

_UNKNOWN_SPEEDS = ("unknown", "")
_NONE = ("none_evident", "", None)


def _speed_block(record: dict[str, Any]) -> dict[str, Any] | None:
    layer2 = record.get("layer2")
    if not isinstance(layer2, dict):
        return None
    speed = layer2.get("speed_differential")
    return speed if isinstance(speed, dict) else None


def _speed_is_gap(speed: dict[str, Any]) -> bool:
    """True when the mandatory block carries no evidence at all (explicit gap)."""
    return (
        speed.get("side_a_processing", "unknown") in _UNKNOWN_SPEEDS
        and speed.get("side_b_processing", "unknown") in _UNKNOWN_SPEEDS
        and speed.get("probe_intent") in _NONE
        and speed.get("differential_exploited") in _NONE
    )


def analyze_gaps(store: SliceStore) -> dict[str, Any]:
    """Sweep stored assessments for ASSSIB gaps; machine-readable report.

    Returns ``{atom_count, assessed, gated, speed_gaps, signals_without_speed,
    missing_party_ids, speed_edges, gap_rate, findings, questions,
    retrieval_priorities}``. ``retrieval_priorities`` is only populated when
    gaps exist (FR-ASSSIB-05).
    """
    assessments = store.assessments()
    gated = 0
    assessed = 0
    speed_gaps: list[str] = []
    signals_without_speed: list[str] = []
    missing_party_ids: list[str] = []

    for record in assessments:
        atom_id = str((record.get("atom") or {}).get("atom_id", "?"))
        speed = _speed_block(record)
        if speed is None:
            gated += 1
            continue
        assessed += 1
        signals = (record.get("layer1") or {}).get("sensemaking_signals") or []
        if _speed_is_gap(speed):
            speed_gaps.append(atom_id)
            if signals:
                # Layer 1 saw speed talk, yet Layer 2 recorded nothing — the
                # sharpest gap: evidence was present but not assessed.
                signals_without_speed.append(atom_id)
        if not speed.get("side_a_party_id") and not speed.get("side_b_party_id"):
            missing_party_ids.append(atom_id)

    findings: list[dict[str, Any]] = []
    if speed_gaps:
        findings.append({
            "kind": "speed_gap",
            "note": f"{len(speed_gaps)} of {assessed} assessed atoms carry an "
            "explicit none_evident speed block — relative processing speeds "
            "are unassessed for them.",
            "atom_ids": speed_gaps,
        })
    if signals_without_speed:
        findings.append({
            "kind": "signal_without_speed",
            "note": f"{len(signals_without_speed)} atoms flagged sensemaking "
            "signals at Layer 1 but recorded no speed evidence at Layer 2 — "
            "assess these first.",
            "atom_ids": signals_without_speed,
        })
    if assessed and len(missing_party_ids) == assessed:
        findings.append({
            "kind": "no_party_linkage",
            "note": "No assessed atom links its speed block to coherence-profile "
            "party ids — collective LCD constraints cannot bind.",
            "atom_ids": [],
        })

    gap_rate = round(len(speed_gaps) / assessed, 3) if assessed else 0.0
    return {
        "atom_count": len(assessments),
        "assessed": assessed,
        "gated": gated,
        "speed_gaps": len(speed_gaps),
        "signals_without_speed": len(signals_without_speed),
        "missing_party_ids": len(missing_party_ids),
        "speed_edges": sum(1 for e in store.graph_edges() if e.get("kind") in SPEED_GRAPH_EDGES),
        "gap_rate": gap_rate,
        "findings": findings,
        "questions": list(GAP_ANALYSIS_QUESTIONS),
        "retrieval_priorities": list(RETRIEVAL_PRIORITIES) if findings else [],
    }
