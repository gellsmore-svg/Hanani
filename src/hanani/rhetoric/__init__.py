"""Rhetorical logic semantic graph — Layer 1 fallacy and audit pattern registry."""

from __future__ import annotations

RHETORIC_GRAPH_VERSION = "0.2"
RHETORIC_DOC = "docs/ontology/rhetorical-logic-graph.md"

AUDIT_CRITERIA: tuple[str, ...] = (
    "audit.chain_completeness",
    "audit.evidence_integration",
    "audit.qualifiers_falsifiability",
    "audit.analytical_intent",
    "audit.update_signals",
    "audit.sensemaking_speed_signals",
)

SENSEMAKING_SIGNAL_KEYWORDS: tuple[str, ...] = (
    "reaction time",
    "coordination",
    "ambiguous",
    "leak",
    "probe",
    "sensational",
    "over-react",
    "under-react",
    "sensemaking",
    "processing speed",
)

ARGUMENT_ROLES: tuple[str, ...] = (
    "arg.premise",
    "arg.warrant",
    "arg.conclusion",
    "arg.qualifier",
    "arg.rebuttal",
    "arg.enthymeme",
)

ROBUSTNESS_TIERS: tuple[str, ...] = (
    "robust.strong",
    "robust.moderate",
    "robust.weak",
)

FALLACIES: dict[str, str] = {
    "fallacy.affirming_consequent": "If A then B; B; therefore A",
    "fallacy.denying_antecedent": "If A then B; not A; therefore not B",
    "fallacy.false_dilemma": "Only two options when more exist",
    "fallacy.equivocation": "Key term shifts meaning mid-argument",
    "fallacy.circular_reasoning": "Conclusion assumed in premise",
    "fallacy.cherry_picking": "Confirming evidence only",
    "fallacy.hasty_generalization": "Broad claim from thin sample",
    "fallacy.anecdotal": "Single story → general law",
    "fallacy.survivorship_bias": "Visible successes; invisible failures",
    "fallacy.base_rate_neglect": "Ignores prior probability",
    "fallacy.post_hoc": "Sequence mistaken for causation",
    "fallacy.single_cause": "One factor explains complex outcome",
    "fallacy.slippery_slope": "Unwarranted escalation chain",
    "fallacy.false_balance": "False equivalence of evidence weight",
    "fallacy.teleology": "Outcome assumed inevitable from narrative arc",
    "fallacy.appeal_to_authority_in_text": "Conclusion rests on cited authority in argument",
    "fallacy.appeal_to_common_belief": "Consensus or 'everyone knows' substitutes for evidence",
    "fallacy.ad_hominem_in_text": "Attacks actor not claim as stated in text",
    "fallacy.genetic": "Dismisses claim by origin alone in text",
    "fallacy.motivated_skepticism": "Asymmetric standards for confirming vs. disconfirming",
    "fallacy.mirror_imaging": "Assumes adversary shares own values/calculus",
    "fallacy.analogy_misuse": "Historical analogy without mechanism match",
    "fallacy.capability_intent_conflation": "Capacity → intent without intermediate reasoning",
    "fallacy.rhetoric_action_conflation": "Cheap talk treated as costly signal",
    "fallacy.unitary_actor": "Ignores bureaucratic/coalitional structure",
    "fallacy.presentism": "Past actors judged anachronistically",
    "fallacy.narrative_closure": "Story completeness substituted for causal proof",
}

ENTHYMEME_PATTERNS: dict[str, str] = {
    "enthymeme.risk_neutral_adversary": "Opponent maximizes same utility function",
    "enthymeme.static_preferences": "Preferences don't shift with losses/gains",
    "enthymeme.credible_threat_assumed": "Threat believed without commitment mechanism",
    "enthymeme.domestic_unified": "Leader speaks for all domestic veto players",
    "enthymeme.linear_escalation": "Escalation ladder fixed and shared",
}

RHETORIC_EDGE_TYPES: tuple[str, ...] = (
    "subtype_of",
    "violates",
    "exhibits",
    "missing_warrant",
    "supports_chain",
    "undermines",
    "detected_in",
    "contradicts",
)


def list_fallacies() -> dict[str, str]:
    return dict(FALLACIES)


def list_enthymemes() -> dict[str, str]:
    return dict(ENTHYMEME_PATTERNS)


def admissible_for_inference(robustness: str) -> bool:
    return robustness in {"robust.strong", "robust.moderate", "Strong", "Moderate"}


__all__ = [
    "ARGUMENT_ROLES",
    "AUDIT_CRITERIA",
    "SENSEMAKING_SIGNAL_KEYWORDS",
    "ENTHYMEME_PATTERNS",
    "FALLACIES",
    "RHETORIC_DOC",
    "RHETORIC_EDGE_TYPES",
    "RHETORIC_GRAPH_VERSION",
    "ROBUSTNESS_TIERS",
    "admissible_for_inference",
    "list_enthymemes",
    "list_fallacies",
]