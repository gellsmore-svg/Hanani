"""Living semantic ontology for geopolitical reasoning (see docs/ontology/)."""

from __future__ import annotations

ONTOLOGY_VERSION = "0.3"
ONTOLOGY_DOC = "docs/ontology/living-semantic-model.md"

# Cross-cutting dynamics (primary layer noted; all cross-cut multiple layers).
CROSS_CUTTING_DYNAMICS: dict[str, dict[str, str | list[str]]] = {
    "asymmetric_sensemaking_speed_informational_brinkmanship": {
        "short": "ASSSIB",
        "primary_layer": "L5_emergent_dynamic",
        "description": (
            "Probing and ambiguity maneuvers targeting relative speed, precision, and "
            "coherence of adversary/alliance sensemaking — informational brinkmanship."
        ),
        "links": [
            "L3_agentic_psychological.jervis_perception_misperception",
            "L3_agentic_psychological.prospect_theory_loss_aversion",
            "L3_agentic_psychological.mental_simulation_counterfactuals",
            "L4_communicative_signaling.cheap_talk_costly_signaling",
            "L4_communicative_signaling.schelling_focal_points",
            "L4_communicative_signaling.credible_commitments",
            "L2_institutional_coalitional.two_level_games",
            "L2_institutional_coalitional.selectorate_winning_coalition",
            "L5_emergent_dynamic.feedback_loops_spirals",
        ],
    },
}

PROBE_INTENTS: tuple[str, ...] = (
    "measure_reaction_speed",
    "measure_model_precision",
    "deliberate_ambiguity",
    "none_evident",
)

PROCESSING_SPEED: tuple[str, ...] = ("fast", "slow", "unknown")

COHERENCE_LEVELS: tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "fragmented",
    "unknown",
)

PARTY_TYPES: tuple[str, ...] = (
    "individual_state",
    "individual_leader",
    "individual_agency",
    "collective_alliance",
    "collective_union",
)

COHERENCE_GRAPH_EDGES: tuple[str, ...] = (
    "constrains_collective_speed",
    "constrains_collective_coherence",
    "lcd_binding_member",
    "observed_in_article",
    "profile_trajectory",
)

SPEED_GRAPH_EDGES: tuple[str, ...] = (
    "processes_faster_than",
    "probes_sensemaking_speed",
    "creates_ambiguity_to_slow",
    "exploits_speed_differential",
)

LAYERS: dict[str, list[str]] = {
    "L1_superstructure": [
        "international_anarchy_security_dilemma",
        "power_distribution_polarity",
        "nuclear_deterrence_mad",
        "economic_interdependence_sanctions_kleptocracy",
        "geographic_strategic_fundamentals",
        "schelling_mixed_motive",
    ],
    "L2_institutional_coalitional": [
        "selectorate_winning_coalition",
        "two_level_games",
        "bureaucratic_politics",
        "information_narrative_control",
        "path_dependence_critical_junctures",
        "putnam_entanglement",
    ],
    "L3_agentic_psychological": [
        "prospect_theory_loss_aversion",
        "cognitive_biases_heuristics",
        "personality_dark_triad",
        "emotional_motivational_drivers",
        "mental_simulation_counterfactuals",
        "jervis_perception_misperception",
        "historical_analogies",
    ],
    "L4_communicative_signaling": [
        "cheap_talk_costly_signaling",
        "madman_unpredictability",
        "brinkmanship_escalation_dominance",
        "audience_targeting",
        "propaganda_narrative_warfare",
        "schelling_focal_points",
        "credible_commitments",
    ],
    "L5_emergent_dynamic": [
        "game_structures_pd_chicken_repeated",
        "feedback_loops_spirals",
        "face_saving_dissonance",
        "path_dependence_hubris_overreach",
        "personalist_pathology_enablement",
        "moral_emergence_inhumane_outcomes",
        "jervis_spiral_vs_deterrence_runtime",
        "schelling_commitment_erosion",
        "asymmetric_sensemaking_speed_informational_brinkmanship",
    ],
}

HISTORICAL_ANCHORS: tuple[str, ...] = (
    "cuban_missile_crisis_1962",
    "russia_ukraine_2014_2022_plus",
    "baltic_alliance_probe_template",
    "napoleonic_overextension",
    "hormuz_chokepoint",
)

ROBUSTNESS_LEVELS: tuple[str, ...] = ("Strong", "Moderate", "Weak")

ATOM_TYPES: tuple[str, ...] = (
    "assertion",
    "causal_claim",
    "analogy",
    "intent_assessment",
    "counterfactual",
    "warrant",
    "premise",
)

GRAPH_EDGE_TYPES: tuple[str, ...] = (
    "agrees",
    "contradicts",
    "complements",
    "implies",
    "gap",
    "supports",
    "weakens",
    *SPEED_GRAPH_EDGES,
    *COHERENCE_GRAPH_EDGES,
)


def list_layers() -> dict[str, list[str]]:
    return {k: list(v) for k, v in LAYERS.items()}


__all__ = [
    "ATOM_TYPES",
    "COHERENCE_GRAPH_EDGES",
    "COHERENCE_LEVELS",
    "CROSS_CUTTING_DYNAMICS",
    "GRAPH_EDGE_TYPES",
    "HISTORICAL_ANCHORS",
    "LAYERS",
    "ONTOLOGY_DOC",
    "ONTOLOGY_VERSION",
    "PARTY_TYPES",
    "PROBE_INTENTS",
    "PROCESSING_SPEED",
    "ROBUSTNESS_LEVELS",
    "SPEED_GRAPH_EDGES",
    "list_layers",
]