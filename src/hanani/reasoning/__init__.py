"""Reasoning engine — layered atom assessment (rhetoric then mechanisms)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from hanani.ontology import (
    COHERENCE_LEVELS,
    CROSS_CUTTING_DYNAMICS,
    LAYERS,
    PROBE_INTENTS,
    PROCESSING_SPEED,
    list_layers,
)
from hanani.rhetoric import (
    AUDIT_CRITERIA,
    FALLACIES,
    RHETORIC_GRAPH_VERSION,
    admissible_for_inference,
)

REASONING_VERSION = "0.3"
REASONING_DOC = "docs/reasoning-system.md"


@dataclass
class RhetoricAssessment:
    """Layer 1 — fallacy graph hits and robustness tier."""

    robustness: str  # Strong | Moderate | Weak
    fallacy_hits: list[str] = field(default_factory=list)
    enthymeme_hits: list[str] = field(default_factory=list)
    # bool when a criterion was actually evaluated; None = unassessed
    # (scaffold must not write fabricated True passes — review H2).
    audit_scores: dict[str, bool | None] = field(default_factory=dict)
    sensemaking_signals: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def admissible_for_inference(self) -> bool:
        return admissible_for_inference(self.robustness)


@dataclass
class SpeedDifferentialAssessment:
    """Mandatory per-atom sensemaking speed analysis (ASSSIB)."""

    side_a_processing: str = "unknown"
    side_b_processing: str = "unknown"
    side_a_coherence: str = "unknown"
    side_b_coherence: str = "unknown"
    side_a_party_id: str | None = None
    side_b_party_id: str | None = None
    differential_exploited: str = "none_evident"
    probe_intent: str = "none_evident"
    notes: str = "none evident — explicit gap"

    def __post_init__(self) -> None:
        if self.side_a_processing not in PROCESSING_SPEED:
            raise ValueError(f"side_a_processing must be one of {PROCESSING_SPEED}")
        if self.side_b_processing not in PROCESSING_SPEED:
            raise ValueError(f"side_b_processing must be one of {PROCESSING_SPEED}")
        if self.side_a_coherence not in COHERENCE_LEVELS:
            raise ValueError(f"side_a_coherence must be one of {COHERENCE_LEVELS}")
        if self.side_b_coherence not in COHERENCE_LEVELS:
            raise ValueError(f"side_b_coherence must be one of {COHERENCE_LEVELS}")
        if self.probe_intent not in PROBE_INTENTS:
            raise ValueError(f"probe_intent must be one of {PROBE_INTENTS}")


@dataclass
class MechanismAssessment:
    """Layer 2 — exhaustive mechanism tags with justifications."""

    tags: list[str] = field(default_factory=list)
    justifications: dict[str, str] = field(default_factory=dict)
    factor_links: list[str] = field(default_factory=list)
    historical_anchors: list[str] = field(default_factory=list)
    speed_differential: SpeedDifferentialAssessment = field(default_factory=SpeedDifferentialAssessment)
    notes: list[str] = field(default_factory=list)


@dataclass
class LogicAtom:
    atom_id: str
    source_id: str
    text: str
    atom_type: str = "assertion"


@dataclass
class AtomAssessmentRecord:
    """Full pipeline output per atom (Phases 1–2)."""

    atom: LogicAtom
    layer1: RhetoricAssessment | None = None
    layer2: MechanismAssessment | None = None
    assessment_summary: str | None = None  # Phase 2 narrative digest
    engine_version: str = REASONING_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReasoningEngine:
    """Scaffold: Layer 1 → Layer 2 pipeline. LLM/rule hooks plug in later."""

    mechanism_registry: dict[str, list[str]] = field(default_factory=lambda: dict(LAYERS))

    def assess_layer1(self, atom: LogicAtom, *, rhetoric_hits: list[str] | None = None) -> RhetoricAssessment:
        """Placeholder: real implementation runs rhetorical graph matcher."""
        hits = rhetoric_hits or []
        valid_hits = [h for h in hits if h in FALLACIES or h.startswith("enthymeme.")]
        robustness = "Weak" if valid_hits else "Moderate"
        if not valid_hits and not hits:
            robustness = "Strong"
        from hanani.rhetoric import SENSEMAKING_SIGNAL_KEYWORDS

        lower = atom.text.lower()
        signals = [kw for kw in SENSEMAKING_SIGNAL_KEYWORDS if kw in lower]
        return RhetoricAssessment(
            robustness=robustness,
            fallacy_hits=[h for h in valid_hits if h.startswith("fallacy.")],
            enthymeme_hits=[h for h in valid_hits if h.startswith("enthymeme.")],
            # Unassessed, not a free pass — same idiom as speed_differential's
            # none_evident (review H2).
            audit_scores={c: None for c in AUDIT_CRITERIA},
            sensemaking_signals=signals,
            notes=["Layer 1 scaffold — replace with graph traversal + LLM audit"],
        )

    def assess_layer2(
        self,
        atom: LogicAtom,
        layer1: RhetoricAssessment,
        *,
        mechanism_tags: list[str] | None = None,
        justifications: dict[str, str] | None = None,
        speed: SpeedDifferentialAssessment | None = None,
    ) -> MechanismAssessment | None:
        if not layer1.admissible_for_inference:
            return None
        tags = list(mechanism_tags or [])
        if layer1.sensemaking_signals and "asymmetric_sensemaking_speed_informational_brinkmanship" not in tags:
            tags.append("asymmetric_sensemaking_speed_informational_brinkmanship")
        return MechanismAssessment(
            tags=tags,
            justifications=justifications or {},
            speed_differential=speed or SpeedDifferentialAssessment(),
            notes=["Layer 2 scaffold — exhaustive tagger not yet wired"],
        )

    def assess_atom(
        self,
        atom: LogicAtom,
        *,
        rhetoric_hits: list[str] | None = None,
        mechanism_tags: list[str] | None = None,
        justifications: dict[str, str] | None = None,
        speed: SpeedDifferentialAssessment | None = None,
    ) -> AtomAssessmentRecord:
        layer1 = self.assess_layer1(atom, rhetoric_hits=rhetoric_hits)
        layer2 = self.assess_layer2(
            atom,
            layer1,
            mechanism_tags=mechanism_tags,
            justifications=justifications,
            speed=speed,
        )
        return AtomAssessmentRecord(atom=atom, layer1=layer1, layer2=layer2)

    def registry_summary(self) -> dict[str, Any]:
        return {
            "reasoning_version": REASONING_VERSION,
            "rhetoric_graph_version": RHETORIC_GRAPH_VERSION,
            "mechanism_layers": list_layers(),
            "audit_criteria_count": len(AUDIT_CRITERIA),
            # Criteria are declared; Layer-1 scaffold does not evaluate them yet
            # (audit_scores are None/unassessed — review H2).
            "audit_criteria_evaluated": False,
            "fallacy_pattern_count": len(FALLACIES),
            "cross_cutting_dynamics": list(CROSS_CUTTING_DYNAMICS.keys()),
        }


def default_engine() -> ReasoningEngine:
    return ReasoningEngine()


__all__ = [
    "AtomAssessmentRecord",
    "LogicAtom",
    "MechanismAssessment",
    "REASONING_DOC",
    "REASONING_VERSION",
    "ReasoningEngine",
    "RhetoricAssessment",
    "SpeedDifferentialAssessment",
    "default_engine",
]