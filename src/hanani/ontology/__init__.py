"""Living semantic ontology for geopolitical reasoning (see docs/ontology/)."""

from __future__ import annotations

ONTOLOGY_VERSION = "0.1"
ONTOLOGY_DOC = "docs/ontology/living-semantic-model.md"

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
    ],
}

HISTORICAL_ANCHORS: tuple[str, ...] = (
    "cuban_missile_crisis_1962",
    "russia_ukraine_2014_2022_plus",
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
)


def list_layers() -> dict[str, list[str]]:
    return {k: list(v) for k, v in LAYERS.items()}


__all__ = [
    "ATOM_TYPES",
    "GRAPH_EDGE_TYPES",
    "HISTORICAL_ANCHORS",
    "LAYERS",
    "ONTOLOGY_DOC",
    "ONTOLOGY_VERSION",
    "ROBUSTNESS_LEVELS",
    "list_layers",
]