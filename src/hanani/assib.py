"""ASSSIB — Asymmetric Sensemaking Speed & Informational Brinkmanship hooks."""

from __future__ import annotations

from typing import Any

from hanani.graph import GraphEdge
from hanani.ontology import CROSS_CUTTING_DYNAMICS, SPEED_GRAPH_EDGES
from hanani.reasoning import AtomAssessmentRecord, SpeedDifferentialAssessment

ASSSIB_ID = "asymmetric_sensemaking_speed_informational_brinkmanship"
ASSSIB_SHORT = "ASSSIB"

# Normative gap-analysis questions (FR-ASSSIB-04 / augmentation prompt step 2).
GAP_ANALYSIS_QUESTIONS: tuple[str, ...] = (
    "What do current atoms imply about relative processing speeds between key actors?",
    "What do current atoms imply about sensemaking quality (coherence) between key actors?",
    "Where are speed or coherence differentials being created or exploited?",
    "Which collective LCD binding members explain observed coordination lag?",
    "Do per-source article histories show degrading alliance coherence over time?",
)

# Active retrieval priorities when ASSSIB gaps exist (FR-ASSSIB-05).
RETRIEVAL_PRIORITIES: tuple[str, ...] = (
    "alliance coordination lag and reaction-time reporting",
    "probe/leak dynamics and sensational framing analysis",
    "domestic vs. international processing-speed mismatches (two-level games)",
    "how sides model each other's sensemaking speed",
    "troop-movement vs. rhetoric disambiguation (cheap talk vs. costly signal)",
)

# Mandatory per-atom speed assessment prompts (FR-ASSSIB-03).
ATOM_SPEED_PROMPTS: tuple[str, ...] = (
    "Does this atom assume fast or slow sensemaking on Side A or Side B?",
    "Is probing intended to measure reaction speed, model precision, or create ambiguity?",
    "If none evident — record none_evident explicitly as a gap signal.",
)


def asssib_metadata() -> dict[str, Any]:
    return {
        "canonical_id": ASSSIB_ID,
        "short": ASSSIB_SHORT,
        **CROSS_CUTTING_DYNAMICS[ASSSIB_ID],
        "speed_graph_edges": list(SPEED_GRAPH_EDGES),
        "gap_questions": list(GAP_ANALYSIS_QUESTIONS),
        "retrieval_priorities": list(RETRIEVAL_PRIORITIES),
        "atom_prompts": list(ATOM_SPEED_PROMPTS),
    }


def speed_edges_from_assessment(
    record: AtomAssessmentRecord,
    *,
    side_a_id: str = "side_a",
    side_b_id: str = "side_b",
    signal_id: str | None = None,
) -> list[GraphEdge]:
    """Emit analysis-graph speed-differential edges from an assessment record (FR-ASSSIB-06)."""
    if record.layer2 is None:
        return []

    speed = record.layer2.speed_differential
    atom_id = record.atom.atom_id
    signal = signal_id or atom_id
    edges: list[GraphEdge] = []

    if speed.probe_intent != "none_evident":
        edges.append(
            GraphEdge(
                source=signal,
                target=side_b_id,
                kind="probes_sensemaking_speed",
                properties={"probe_intent": speed.probe_intent, "atom_id": atom_id},
            )
        )

    if speed.differential_exploited not in ("none_evident", "", "parity"):
        faster, slower = _exploitation_pair(speed, side_a_id, side_b_id)
        if faster and slower:
            edges.append(
                GraphEdge(
                    source=faster,
                    target=slower,
                    kind="exploits_speed_differential",
                    properties={"atom_id": atom_id, "notes": speed.notes},
                )
            )
            edges.append(
                GraphEdge(
                    source=faster,
                    target=slower,
                    kind="processes_faster_than",
                    properties={"atom_id": atom_id},
                )
            )

    if speed.probe_intent == "deliberate_ambiguity":
        edges.append(
            GraphEdge(
                source=signal,
                target=side_b_id,
                kind="creates_ambiguity_to_slow",
                properties={"atom_id": atom_id},
            )
        )

    return edges


def _exploitation_pair(
    speed: SpeedDifferentialAssessment,
    side_a_id: str,
    side_b_id: str,
) -> tuple[str | None, str | None]:
    exploited = speed.differential_exploited.lower()
    if "a_faster" in exploited or exploited == "a":
        return side_a_id, side_b_id
    if "b_faster" in exploited or exploited == "b":
        return side_b_id, side_a_id
    if speed.side_a_processing == "fast" and speed.side_b_processing == "slow":
        return side_a_id, side_b_id
    if speed.side_b_processing == "fast" and speed.side_a_processing == "slow":
        return side_b_id, side_a_id
    return None, None


def readiness() -> dict[str, Any]:
    """ASSSIB schema readiness vs operational wiring (review F3).

    Schema fields and gap analysis are in place; coherence profiles and
    collective LCD exist as scaffolds and are not auto-wired into ingest.
    """
    return {
        # Backward-compatible: "ready" means the ASSSIB *schema* is present.
        "ready": True,
        "schema_ready": True,
        "operationally_wired": False,
        "dynamic": ASSSIB_ID,
        "first_class_speed_differential": True,
        "mandatory_per_atom": True,
        "coherence_profiles": True,  # module/API present (scaffold)
        "collective_lcd": True,  # module/API present (scaffold)
        "coherence_auto_wired_in_ingest": False,
        "collective_lcd_auto_wired_in_ingest": False,
        "message": (
            "ASSSIB schema is ready: every atom carries a mandatory "
            "speed_differential block (none_evident when no evidence), and "
            "`hanani gaps` reports coverage honestly. Coherence profiles and "
            "collective LCD exist as scaffolds and are not auto-wired into "
            "ingest yet — check `hanani coherence` / `hanani gaps` for "
            "operational state before treating the store as party-linked."
        ),
    }


__all__ = [
    "ASSSIB_ID",
    "ASSSIB_SHORT",
    "ATOM_SPEED_PROMPTS",
    "GAP_ANALYSIS_QUESTIONS",
    "RETRIEVAL_PRIORITIES",
    "asssib_metadata",
    "readiness",
    "speed_edges_from_assessment",
]