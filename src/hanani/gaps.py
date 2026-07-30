"""Registry-aware gap analysis over the persisted corpus (FR-ANALYSIS-02).

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
from hanani.ontology import LAYERS, SPEED_GRAPH_EDGES
from hanani.rhetoric import ENTHYMEME_PATTERNS, FALLACIES
from hanani.store import SliceStore

_UNKNOWN_SPEEDS = ("unknown", "")
_NONE = ("none_evident", "", None)
_ASSSIB_TAG = "asymmetric_sensemaking_speed_informational_brinkmanship"


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


def _registry_coverage(assessments: list[dict[str, Any]]) -> dict[str, Any]:
    """Report observed registry coverage without treating absence as disproof."""
    mechanisms = {tag for layer in LAYERS.values() for tag in layer}
    rhetoric = set(FALLACIES) | set(ENTHYMEME_PATTERNS)
    covered_mechanisms: set[str] = set()
    covered_rhetoric: set[str] = set()

    for record in assessments:
        layer2 = record.get("layer2") or {}
        covered_mechanisms.update(set(layer2.get("tags") or []) & mechanisms)
        layer1 = record.get("layer1") or {}
        covered_rhetoric.update(set(layer1.get("fallacy_hits") or []) & rhetoric)
        covered_rhetoric.update(set(layer1.get("enthymeme_hits") or []) & rhetoric)

    by_layer = {
        layer: {
            "total": len(tags),
            "covered": sorted(set(tags) & covered_mechanisms),
            "uncovered": sorted(set(tags) - covered_mechanisms),
        }
        for layer, tags in LAYERS.items()
    }
    return {
        "mechanisms": {
            "total": len(mechanisms),
            "covered": sorted(covered_mechanisms),
            "uncovered": sorted(mechanisms - covered_mechanisms),
            "coverage_rate": round(len(covered_mechanisms) / len(mechanisms), 3),
            "by_layer": by_layer,
        },
        "rhetoric": {
            "total": len(rhetoric),
            "covered": sorted(covered_rhetoric),
            "uncovered": sorted(rhetoric - covered_rhetoric),
            "coverage_rate": round(len(covered_rhetoric) / len(rhetoric), 3),
        },
    }


def _asssib_history_gaps(assessments: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Find thin source and party histories where ASSSIB signals are present."""
    source_articles: dict[str, set[str]] = {}
    party_articles: dict[str, set[str]] = {}
    for record in assessments:
        layer1 = record.get("layer1") or {}
        layer2 = record.get("layer2") or {}
        tags = set(layer2.get("tags") or [])
        if not layer1.get("sensemaking_signals") and _ASSSIB_TAG not in tags:
            continue
        article_id = str(record.get("article_id") or "?")
        source_id = str((record.get("atom") or {}).get("source_id") or "?")
        source_articles.setdefault(source_id, set()).add(article_id)
        speed = _speed_block(record) or {}
        for party_id in (speed.get("side_a_party_id"), speed.get("side_b_party_id")):
            if party_id:
                party_articles.setdefault(str(party_id), set()).add(article_id)

    return {
        "source_history": [
            {"source_id": source_id, "article_count": len(article_ids)}
            for source_id, article_ids in sorted(source_articles.items())
            if len(article_ids) < 2
        ],
        "party_trajectory": [
            {"party_id": party_id, "article_count": len(article_ids)}
            for party_id, article_ids in sorted(party_articles.items())
            if len(article_ids) < 2
        ],
    }


def analyze_gaps(store: SliceStore) -> dict[str, Any]:
    """Sweep assessments for ASSSIB and registry coverage gaps.

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

    coverage = _registry_coverage(assessments)
    history_gaps = _asssib_history_gaps(assessments)
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
    for layer, detail in coverage["mechanisms"]["by_layer"].items():
        if assessments and not detail["covered"]:
            findings.append({
                "kind": "mechanism_layer_gap",
                "note": f"No admissible atom is tagged to {layer}; seek evidence that can test its registered mechanisms.",
                "layer": layer,
                "information_need": f"Evidence bearing mechanisms in {layer}.",
            })
    if history_gaps["source_history"]:
        findings.append({
            "kind": "source_history_gap",
            "note": "ASSSIB signals appear in sources with fewer than two articles, so a trajectory cannot yet be compared.",
            "sources": history_gaps["source_history"],
            "information_need": "Follow-up reporting from the same sources to compare processing-speed and coherence over time.",
        })
    if history_gaps["party_trajectory"]:
        findings.append({
            "kind": "party_trajectory_gap",
            "note": "Party-linked ASSSIB observations have fewer than two articles, so coherence trajectories remain thin.",
            "parties": history_gaps["party_trajectory"],
            "information_need": "Additional party-linked observations to establish reaction-speed and coherence trajectories.",
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
        "registry_coverage": coverage,
        "asssib_history_gaps": history_gaps,
        "findings": findings,
        "questions": list(GAP_ANALYSIS_QUESTIONS),
        "retrieval_priorities": list(RETRIEVAL_PRIORITIES) if findings else [],
    }
