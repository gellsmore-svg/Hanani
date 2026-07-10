"""Tests for coherence speed profiles and collective LCD (FR-COHERENCE-*)."""

from __future__ import annotations

from datetime import datetime, timezone

from hanani.coherence import (
    CoherenceRegistry,
    compute_lcd_coherence,
    compute_lcd_speed,
)
from hanani.reasoning import LogicAtom, SpeedDifferentialAssessment, default_engine
from hanani.sources import SourceCorpus


def _registry_with_nato() -> CoherenceRegistry:
    reg = CoherenceRegistry()
    reg.register_party(party_id="de", party_type="individual_state", label="Germany")
    reg.register_party(party_id="pl", party_type="individual_state", label="Poland")
    reg.register_party(party_id="ee", party_type="individual_state", label="Estonia")
    reg.define_collective(
        collective_id="nato-frontline-bloc",
        label="NATO frontline bloc",
        member_ids=["de", "pl", "ee"],
    )
    return reg


def test_lcd_speed_picks_slowest_member() -> None:
    reg = _registry_with_nato()
    reg.record_observation(
        "de",
        observed_at="2026-07-01T00:00:00Z",
        source_id="src-1",
        article_id="art-1",
        reaction_speed="fast",
        coherence="high",
    )
    reg.record_observation(
        "pl",
        observed_at="2026-07-01T00:00:00Z",
        source_id="src-1",
        article_id="art-1",
        reaction_speed="slow",
        coherence="medium",
    )
    reg.record_observation(
        "ee",
        observed_at="2026-07-01T00:00:00Z",
        source_id="src-1",
        article_id="art-1",
        reaction_speed="fast",
        coherence="high",
    )

    collective = reg.collectives["nato-frontline-bloc"]
    assert collective.lcd_reaction_speed == "slow"
    assert collective.lcd_speed_member == "pl"


def test_lcd_coherence_picks_most_fragmented_member() -> None:
    reg = _registry_with_nato()
    reg.record_observation(
        "de",
        observed_at="2026-07-02T00:00:00Z",
        source_id="src-1",
        article_id="art-2",
        reaction_speed="fast",
        coherence="high",
    )
    reg.record_observation(
        "pl",
        observed_at="2026-07-02T00:00:00Z",
        source_id="src-1",
        article_id="art-2",
        reaction_speed="fast",
        coherence="fragmented",
    )
    reg.record_observation(
        "ee",
        observed_at="2026-07-02T00:00:00Z",
        source_id="src-1",
        article_id="art-2",
        reaction_speed="fast",
        coherence="medium",
    )

    collective = reg.collectives["nato-frontline-bloc"]
    assert collective.lcd_coherence == "fragmented"
    assert collective.lcd_coherence_member == "pl"


def test_profile_trajectory_from_source_history() -> None:
    corpus = SourceCorpus()
    reg = CoherenceRegistry()
    reg.register_party(party_id="eu-commission", party_type="individual_agency", label="EU Commission")

    t1 = datetime(2026, 7, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 7, 8, tzinfo=timezone.utc)
    a1 = corpus.register(
        source_id="analyst-x",
        title="Week 1",
        text="EU slow to coordinate",
        provenance="manual",
        ingested_at=t1,
    )
    a2 = corpus.register(
        source_id="analyst-x",
        title="Week 2",
        text="EU fragmentation worsens",
        provenance="manual",
        ingested_at=t2,
    )

    reg.record_observation(
        "eu-commission",
        observed_at=a1.ingested_at.isoformat(),
        source_id=a1.source_id,
        article_id=a1.article_id,
        reaction_speed="slow",
        coherence="medium",
    )
    reg.record_observation(
        "eu-commission",
        observed_at=a2.ingested_at.isoformat(),
        source_id=a2.source_id,
        article_id=a2.article_id,
        reaction_speed="slow",
        coherence="fragmented",
    )

    profile = reg.individuals["eu-commission"]
    traj = profile.trajectory()
    assert len(traj) == 2
    assert traj[-1]["coherence"] == "fragmented"
    assert corpus.history("analyst-x")[-1].article_id == a2.article_id


def test_ingest_assessment_updates_parties() -> None:
    reg = _registry_with_nato()
    engine = default_engine()
    atom = LogicAtom(
        atom_id="atom-probe",
        source_id="src-leak",
        text="Leak probes whether NATO capitals coordinate within 48 hours.",
    )
    record = engine.assess_atom(
        atom,
        speed=SpeedDifferentialAssessment(
            side_a_processing="slow",
            side_b_processing="fast",
            side_a_coherence="fragmented",
            side_b_coherence="high",
            side_a_party_id="de",
            side_b_party_id="pl",
            differential_exploited="B_faster",
            probe_intent="measure_reaction_speed",
            notes="coordination lag",
        ),
    )
    reg.ingest_assessment(record, article_id="art-probe", side_a_party_id="de", side_b_party_id="pl")

    assert reg.individuals["de"].reaction_speed == "slow"
    assert reg.individuals["de"].coherence == "fragmented"
    assert reg.individuals["pl"].reaction_speed == "fast"


def test_move_context_flags_asssib_risk() -> None:
    reg = _registry_with_nato()
    reg.record_observation(
        "pl",
        observed_at="2026-07-03T00:00:00Z",
        source_id="src-1",
        article_id="art-3",
        reaction_speed="slow",
        coherence="fragmented",
    )
    reg.record_observation(
        "de",
        observed_at="2026-07-03T00:00:00Z",
        source_id="src-1",
        article_id="art-3",
        reaction_speed="fast",
        coherence="high",
    )
    reg.record_observation(
        "ee",
        observed_at="2026-07-03T00:00:00Z",
        source_id="src-1",
        article_id="art-3",
        reaction_speed="fast",
        coherence="high",
    )
    reg.recompute_collective("nato-frontline-bloc")

    ctx = reg.move_context(
        "nato-frontline-bloc",
        speed=SpeedDifferentialAssessment(
            side_a_processing="slow",
            side_b_processing="fast",
            probe_intent="measure_reaction_speed",
            differential_exploited="B_faster",
        ),
    )
    assert ctx.asssib_risk == "high"
    assert ctx.binding_coherence_member == "pl"
    assert any("LCD" in n or "fragmented" in n for n in ctx.interpretation_notes)


def test_compute_lcd_helpers_empty() -> None:
    assert compute_lcd_speed([]) == ("unknown", None)
    assert compute_lcd_coherence([]) == ("unknown", None)