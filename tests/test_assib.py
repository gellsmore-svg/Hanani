"""Tests for ASSSIB augmentation (FR-ASSSIB-*)."""

from __future__ import annotations

from hanani.assib import (
    ASSSIB_ID,
    ATOM_SPEED_PROMPTS,
    GAP_ANALYSIS_QUESTIONS,
    RETRIEVAL_PRIORITIES,
    asssib_metadata,
    readiness,
    speed_edges_from_assessment,
)
from hanani.reasoning import LogicAtom, SpeedDifferentialAssessment, default_engine


def test_asssib_in_ontology_registry() -> None:
    meta = asssib_metadata()
    assert meta["canonical_id"] == ASSSIB_ID
    assert meta["short"] == "ASSSIB"
    assert "probes_sensemaking_speed" in meta["speed_graph_edges"]


def test_gap_and_retrieval_constants() -> None:
    assert len(GAP_ANALYSIS_QUESTIONS) >= 3
    assert len(RETRIEVAL_PRIORITIES) >= 3
    assert len(ATOM_SPEED_PROMPTS) == 3


def test_readiness_declares_first_class_speed() -> None:
    info = readiness()
    assert info["ready"] is True
    assert info["schema_ready"] is True
    assert info["operationally_wired"] is False
    assert info["first_class_speed_differential"] is True
    assert info["mandatory_per_atom"] is True
    assert info["coherence_auto_wired_in_ingest"] is False
    assert "schema" in info["message"].lower()


def test_speed_edges_from_probe_assessment() -> None:
    atom = LogicAtom(
        atom_id="atom-1",
        source_id="src-1",
        text="Leak probes NATO reaction within 48 hours.",
    )
    record = default_engine().assess_atom(
        atom,
        speed=SpeedDifferentialAssessment(
            side_a_processing="slow",
            side_b_processing="fast",
            differential_exploited="B_faster",
            probe_intent="measure_reaction_speed",
            notes="coordination lag",
        ),
    )
    edges = speed_edges_from_assessment(
        record,
        side_a_id="nato",
        side_b_id="prober",
    )
    kinds = {e.kind for e in edges}
    assert "probes_sensemaking_speed" in kinds
    assert "exploits_speed_differential" in kinds
    assert "processes_faster_than" in kinds


def test_speed_edges_none_evident_empty() -> None:
    atom = LogicAtom(atom_id="a", source_id="s", text="Static border fact.")
    record = default_engine().assess_atom(atom)
    assert record.layer2 is not None
    edges = speed_edges_from_assessment(record)
    assert edges == []