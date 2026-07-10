"""Coherence speed profiles — individual parties and collective LCD constraints."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from hanani.ontology import COHERENCE_LEVELS, PARTY_TYPES, PROCESSING_SPEED
from hanani.reasoning import AtomAssessmentRecord, SpeedDifferentialAssessment

_SPEED_LCD_ORDER: dict[str, int] = {"slow": 0, "unknown": 1, "fast": 2}
_COHERENCE_LCD_ORDER: dict[str, int] = {
    "fragmented": 0,
    "low": 1,
    "unknown": 2,
    "medium": 3,
    "high": 4,
}


def _validate_speed(value: str) -> None:
    if value not in PROCESSING_SPEED:
        raise ValueError(f"reaction_speed must be one of {PROCESSING_SPEED}")


def _validate_coherence(value: str) -> None:
    if value not in COHERENCE_LEVELS:
        raise ValueError(f"coherence must be one of {COHERENCE_LEVELS}")


def _validate_party_type(value: str) -> None:
    if value not in PARTY_TYPES:
        raise ValueError(f"party_type must be one of {PARTY_TYPES}")


@dataclass
class CoherenceObservation:
    """One evidence point for a party's speed/coherence from a source article."""

    observed_at: str
    source_id: str
    article_id: str
    reaction_speed: str
    coherence: str
    atom_id: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        _validate_speed(self.reaction_speed)
        _validate_coherence(self.coherence)


@dataclass
class CoherenceSpeedProfile:
    """Individual party — reaction speed and internal/coordination coherence."""

    party_id: str
    party_type: str
    label: str
    reaction_speed: str = "unknown"
    coherence: str = "unknown"
    observations: list[CoherenceObservation] = field(default_factory=list)
    member_of: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _validate_party_type(self.party_type)
        _validate_speed(self.reaction_speed)
        _validate_coherence(self.coherence)

    def add_observation(self, obs: CoherenceObservation) -> None:
        self.observations.append(obs)
        self._recompute_from_observations()

    def _recompute_from_observations(self) -> None:
        if not self.observations:
            return
        latest = self.observations[-1]
        self.reaction_speed = latest.reaction_speed
        self.coherence = latest.coherence

    def trajectory(self) -> list[dict[str, str]]:
        return [
            {
                "observed_at": o.observed_at,
                "reaction_speed": o.reaction_speed,
                "coherence": o.coherence,
                "source_id": o.source_id,
                "article_id": o.article_id,
            }
            for o in self.observations
        ]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CollectiveCoherenceProfile:
    """Collective party constrained by lowest-common-denominator (LCD) member."""

    collective_id: str
    label: str
    member_ids: list[str]
    lcd_reaction_speed: str = "unknown"
    lcd_coherence: str = "unknown"
    lcd_speed_member: str | None = None
    lcd_coherence_member: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        _validate_speed(self.lcd_reaction_speed)
        _validate_coherence(self.lcd_coherence)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MoveCoherenceContext:
    """Interpretation hook: how LCD profiles constrain observable collective moves."""

    collective_id: str
    effective_reaction_speed: str
    effective_coherence: str
    binding_speed_member: str | None
    binding_coherence_member: str | None
    asssib_risk: str
    interpretation_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_lcd_speed(profiles: list[CoherenceSpeedProfile]) -> tuple[str, str | None]:
    """Collective moves no faster than the slowest member (LCD on speed)."""
    if not profiles:
        return "unknown", None
    binding = min(profiles, key=lambda p: _SPEED_LCD_ORDER.get(p.reaction_speed, 1))
    return binding.reaction_speed, binding.party_id


def compute_lcd_coherence(profiles: list[CoherenceSpeedProfile]) -> tuple[str, str | None]:
    """Collective coherence no higher than the least coherent member (LCD)."""
    if not profiles:
        return "unknown", None
    binding = min(profiles, key=lambda p: _COHERENCE_LCD_ORDER.get(p.coherence, 2))
    return binding.coherence, binding.party_id


@dataclass
class CoherenceRegistry:
    """Registry of individual and collective coherence-speed profiles."""

    individuals: dict[str, CoherenceSpeedProfile] = field(default_factory=dict)
    collectives: dict[str, CollectiveCoherenceProfile] = field(default_factory=dict)

    def register_party(
        self,
        *,
        party_id: str,
        party_type: str,
        label: str,
        member_of: list[str] | None = None,
    ) -> CoherenceSpeedProfile:
        profile = CoherenceSpeedProfile(
            party_id=party_id,
            party_type=party_type,
            label=label,
            member_of=list(member_of or []),
        )
        self.individuals[party_id] = profile
        return profile

    def define_collective(
        self,
        *,
        collective_id: str,
        label: str,
        member_ids: list[str],
        notes: str = "",
    ) -> CollectiveCoherenceProfile:
        for mid in member_ids:
            if mid not in self.individuals:
                raise KeyError(f"unknown member party: {mid}")
            if collective_id not in self.individuals[mid].member_of:
                self.individuals[mid].member_of.append(collective_id)

        collective = CollectiveCoherenceProfile(
            collective_id=collective_id,
            label=label,
            member_ids=list(member_ids),
            notes=notes,
        )
        self.collectives[collective_id] = collective
        self.recompute_collective(collective_id)
        return collective

    def record_observation(
        self,
        party_id: str,
        *,
        observed_at: str,
        source_id: str,
        article_id: str,
        reaction_speed: str,
        coherence: str,
        atom_id: str | None = None,
        notes: str = "",
    ) -> CoherenceObservation:
        profile = self._require_individual(party_id)
        obs = CoherenceObservation(
            observed_at=observed_at,
            source_id=source_id,
            article_id=article_id,
            atom_id=atom_id,
            reaction_speed=reaction_speed,
            coherence=coherence,
            notes=notes,
        )
        profile.add_observation(obs)
        for collective_id in profile.member_of:
            self.recompute_collective(collective_id)
        return obs

    def recompute_collective(self, collective_id: str) -> CollectiveCoherenceProfile:
        collective = self.collectives[collective_id]
        members = [self.individuals[mid] for mid in collective.member_ids]
        speed, speed_member = compute_lcd_speed(members)
        coherence, coherence_member = compute_lcd_coherence(members)
        collective.lcd_reaction_speed = speed
        collective.lcd_coherence = coherence
        collective.lcd_speed_member = speed_member
        collective.lcd_coherence_member = coherence_member
        return collective

    def ingest_assessment(
        self,
        record: AtomAssessmentRecord,
        *,
        article_id: str,
        side_a_party_id: str | None = None,
        side_b_party_id: str | None = None,
        observed_at: str | None = None,
    ) -> list[CoherenceObservation]:
        """Update party profiles from an atom assessment's speed_differential block."""
        if record.layer2 is None:
            return []

        speed = record.layer2.speed_differential
        ts = observed_at or datetime.now(timezone.utc).isoformat()
        out: list[CoherenceObservation] = []

        mapping = (
            (side_a_party_id, speed.side_a_processing, speed.side_a_coherence),
            (side_b_party_id, speed.side_b_processing, speed.side_b_coherence),
        )
        for party_id, reaction_speed, coherence in mapping:
            if not party_id or party_id not in self.individuals:
                continue
            obs = self.record_observation(
                party_id,
                observed_at=ts,
                source_id=record.atom.source_id,
                article_id=article_id,
                atom_id=record.atom.atom_id,
                reaction_speed=reaction_speed,
                coherence=coherence,
                notes=speed.notes,
            )
            out.append(obs)
        return out

    def move_context(
        self,
        collective_id: str,
        *,
        speed: SpeedDifferentialAssessment | None = None,
    ) -> MoveCoherenceContext:
        """Assess how collective LCD constrains interpretation of current moves (ASSSIB)."""
        collective = self.collectives[collective_id]
        notes: list[str] = []
        risk = "low"

        if collective.lcd_reaction_speed == "slow":
            notes.append("LCD speed is slow — collective vulnerable to fast probes.")
            risk = "elevated"
        if collective.lcd_coherence in ("fragmented", "low"):
            notes.append(
                f"LCD coherence is {collective.lcd_coherence} — "
                "fragmented responses likely; probers may exploit coordination lag."
            )
            risk = "high"

        if speed and speed.differential_exploited not in ("none_evident", ""):
            notes.append(f"Atom reports differential exploited: {speed.differential_exploited}.")
            if risk == "low":
                risk = "elevated"

        if speed and speed.probe_intent not in ("none_evident", ""):
            notes.append(f"Probe intent: {speed.probe_intent} — test against LCD profile.")

        return MoveCoherenceContext(
            collective_id=collective_id,
            effective_reaction_speed=collective.lcd_reaction_speed,
            effective_coherence=collective.lcd_coherence,
            binding_speed_member=collective.lcd_speed_member,
            binding_coherence_member=collective.lcd_coherence_member,
            asssib_risk=risk,
            interpretation_notes=notes,
        )

    def summary(self) -> dict[str, Any]:
        return {
            "individual_count": len(self.individuals),
            "collective_count": len(self.collectives),
            "collectives": {
                cid: {
                    "lcd_reaction_speed": c.lcd_reaction_speed,
                    "lcd_coherence": c.lcd_coherence,
                    "lcd_speed_member": c.lcd_speed_member,
                    "lcd_coherence_member": c.lcd_coherence_member,
                    "member_count": len(c.member_ids),
                }
                for cid, c in sorted(self.collectives.items())
            },
        }

    def _require_individual(self, party_id: str) -> CoherenceSpeedProfile:
        if party_id not in self.individuals:
            raise KeyError(f"unknown party: {party_id}")
        return self.individuals[party_id]


def default_registry() -> CoherenceRegistry:
    return CoherenceRegistry()


__all__ = [
    "CoherenceObservation",
    "CoherenceRegistry",
    "CoherenceSpeedProfile",
    "CollectiveCoherenceProfile",
    "MoveCoherenceContext",
    "compute_lcd_coherence",
    "compute_lcd_speed",
    "default_registry",
]