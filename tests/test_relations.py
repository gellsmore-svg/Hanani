"""Semantic relational mapping between atoms (FR-ANALYSIS-01)."""

from __future__ import annotations

import pytest

from hanani.pipeline import ingest_and_assess
from hanani.relations import map_relations, relate_atoms
from hanani.store import SliceStore

_REUTERS = (
    "Insurance premiums for Black Sea grain shipments rose by roughly a third "
    "after strikes on port infrastructure resumed last month. "
    "Grain transit volumes through the corridor fell fifteen percent in June."
)
_AP = (
    "Black Sea grain shipment insurance premiums have risen by about a third "
    "since port infrastructure strikes resumed last month. "
    "Officials said talks on the export corridor remain stalled in Geneva."
)


def _stored(tmp_path) -> SliceStore:
    store = SliceStore(tmp_path)
    ingest_and_assess(_REUTERS, source_id="reuters", title="R", store=store)
    ingest_and_assess(_AP, source_id="ap", title="A", store=store)
    return store


def test_floor_relations_typed_and_audited(tmp_path) -> None:
    store = _stored(tmp_path)
    edges = relate_atoms(store.assessments())
    kinds = {e["kind"] for e in edges}
    assert "yields" in kinds  # same-article temporal sequence
    # the near-identical premium sentences across sources corroborate
    agrees = [e for e in edges if e["kind"] == "agrees"]
    assert agrees, "expected cross-source corroboration"
    for edge in edges:
        assert edge["properties"]["basis"].startswith(("deterministic:", "model"))
        assert 0.0 <= edge["properties"]["score"] <= 1.0


def test_model_tier_vocabulary_validation(tmp_path) -> None:
    store = _stored(tmp_path)
    records = store.assessments()
    ids = [r["atom"]["atom_id"] for r in records if r["layer2"] is not None][:2]

    def ask(_prompt: str) -> str:
        return (
            '[{"source": "%s", "target": "%s", "kind": "contradicts"},'
            ' {"source": "%s", "target": "%s", "kind": "invented_kind"},'
            ' {"source": "ghost", "target": "%s", "kind": "supports"}]'
            % (ids[0], ids[1], ids[0], ids[1], ids[1])
        )

    edges = relate_atoms(records, ask=ask)
    model_edges = [e for e in edges if e["properties"]["basis"] == "model"]
    assert len(model_edges) == 1  # invented kind + unknown id both dropped
    assert model_edges[0]["kind"] == "contradicts"


def test_bad_model_output_keeps_floor(tmp_path) -> None:
    store = _stored(tmp_path)
    with_model = relate_atoms(store.assessments(), ask=lambda _p: "not json")
    without = relate_atoms(store.assessments())
    assert len(with_model) == len(without)


def test_map_relations_persists_and_summarises(tmp_path) -> None:
    store = _stored(tmp_path)
    report = map_relations(store)
    assert report["scope"] == "corpus" and report["relation_count"] > 0
    persisted = [e for e in store.graph_edges("corpus-relations")]
    assert len(persisted) == report["relation_count"]
    assert store.summary()["graph_edge_count"] >= report["relation_count"]

    with pytest.raises(ValueError, match="unknown article_id"):
        map_relations(store, article_id="nope")


def test_cli_relations(tmp_path, capsys) -> None:
    from hanani.cli import main

    _stored(tmp_path)
    assert main(["relations", "--store", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "edges=" in out and "yields:" in out
