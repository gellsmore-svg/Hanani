"""Vertical slice: ingest → atoms → Layer 1 → Layer 2 → persist."""

from __future__ import annotations

import json

import pytest

from hanani.pipeline import detect_rhetoric_hits, extract_atoms, ingest_and_assess
from hanani.store import SliceStore

# A realistic wire-style excerpt. The final sentence carries a deliberate
# false-dilemma cue so the deterministic Layer-1 floor has something to catch.
_ARTICLE = (
    "Ukrainian officials said three drones struck an oil depot near the port "
    "of Odesa early on Tuesday, igniting a fire that burned for six hours. "
    "Russia's defence ministry did not immediately comment on the reports. "
    "Insurance premiums for Black Sea grain shipments have risen by roughly a "
    "third since the strikes on port infrastructure resumed last month. "
    "Analysts agree the attacks are intended to pressure Kyiv's export economy "
    "ahead of the next round of talks. "
    "The West now has only two options: escalate its support or watch the "
    "corridor close entirely."
)


def test_extract_atoms_deterministic() -> None:
    atoms = extract_atoms(_ARTICLE, source_id="reuters")
    assert 3 <= len(atoms) <= 10
    assert all(a.source_id == "reuters" and a.atom_id.startswith("atom-") for a in atoms)
    # deterministic: same text → same atom ids
    again = extract_atoms(_ARTICLE, source_id="reuters")
    assert [a.atom_id for a in again] == [a.atom_id for a in atoms]


def test_extract_atoms_model_tier_with_fallback() -> None:
    good = extract_atoms(
        _ARTICLE, source_id="s",
        ask=lambda _p: '["Drones struck an oil depot near Odesa.", "Premiums rose by a third."]',
    )
    assert [a.text for a in good] == [
        "Drones struck an oil depot near Odesa.",
        "Premiums rose by a third.",
    ]
    # garbage model output → deterministic floor
    fallback = extract_atoms(_ARTICLE, source_id="s", ask=lambda _p: "not json")
    assert len(fallback) >= 3


def test_detect_rhetoric_hits_cues_and_model_validation() -> None:
    assert "fallacy.false_dilemma" in detect_rhetoric_hits(
        "The West now has only two options: escalate or capitulate."
    )
    assert "fallacy.appeal_to_authority_in_text" in detect_rhetoric_hits(
        "Analysts agree the attacks will continue."
    )
    assert detect_rhetoric_hits("Grain shipments fell by ten percent in June.") == []
    # model tier: known keys accepted, invented keys dropped
    hits = detect_rhetoric_hits(
        "Plain claim.",
        ask=lambda _p: '["fallacy.mirror_imaging", "fallacy.totally_invented"]',
    )
    assert hits == ["fallacy.mirror_imaging"]


def test_ingest_and_assess_end_to_end(tmp_path) -> None:
    store = SliceStore(tmp_path)
    summary = ingest_and_assess(
        _ARTICLE, source_id="reuters", title="Odesa depot strike", store=store,
    )
    assert summary["atom_count"] >= 3
    assert summary["model_tier"] is False

    # Layer-1 gate: cue-hit atoms are Weak and must NOT reach Layer 2.
    records = store.assessments(summary["article_id"])
    assert len(records) == summary["atom_count"]
    weak = [r for r in records if r["layer1"]["robustness"] == "Weak"]
    assert weak, "expected the false-dilemma sentence to be Weak"
    assert all(r["layer2"] is None for r in weak)
    strong_or_moderate = [r for r in records if r["layer1"]["robustness"] != "Weak"]
    assert summary["admissible_atoms"] == len(strong_or_moderate)

    # persisted article record
    articles = store.articles()
    assert len(articles) == 1 and articles[0]["source_id"] == "reuters"
    assert articles[0]["atom_ids"], "atoms linked back to the witness article"

    # store summary aggregates
    agg = store.summary()
    assert agg["article_count"] == 1
    assert agg["atom_count"] == summary["atom_count"]
    assert agg["sources"] == ["reuters"]


def test_ingest_rejects_empty_text(tmp_path) -> None:
    with pytest.raises(ValueError, match="text is required"):
        ingest_and_assess("   ", source_id="s", title="t", store=SliceStore(tmp_path))


def test_store_tolerates_garbage_lines(tmp_path) -> None:
    store = SliceStore(tmp_path)
    store.save_article({"article_id": "a1", "source_id": "s"})
    (tmp_path / "articles.jsonl").open("a").write("{broken json\n")
    assert [a["article_id"] for a in store.articles()] == ["a1"]


def test_cli_ingest_and_corpus(tmp_path, capsys) -> None:
    from hanani.cli import main

    article = tmp_path / "odesa.txt"
    article.write_text(_ARTICLE, encoding="utf-8")
    rc = main([
        "ingest", str(article), "--source-id", "reuters", "--store", str(tmp_path / "store"),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "atoms:" in out and "stored:" in out

    rc = main(["corpus", "--store", str(tmp_path / "store")])
    out = capsys.readouterr().out
    assert rc == 0 and "1 articles" in out


def test_assessment_records_are_json_serialisable(tmp_path) -> None:
    store = SliceStore(tmp_path)
    ingest_and_assess(_ARTICLE, source_id="s", title="t", store=store)
    for record in store.assessments():
        json.dumps(record)  # must not raise


def test_speed_edges_persisted_when_evidence_present(tmp_path) -> None:
    """FR-ASSSIB-06 integration: assessments with speed evidence emit edges."""
    from hanani.reasoning import ReasoningEngine, SpeedDifferentialAssessment

    class SpeedAwareEngine(ReasoningEngine):
        def assess_atom(self, atom, **kwargs):
            kwargs["speed"] = SpeedDifferentialAssessment(
                side_a_processing="fast", side_b_processing="slow",
                differential_exploited="side_a_exploits",
                probe_intent="measure_reaction_speed",
                notes="probe observed",
            )
            return super().assess_atom(atom, **kwargs)

    store = SliceStore(tmp_path)
    summary = ingest_and_assess(
        _ARTICLE, source_id="reuters", title="Odesa", store=store,
        engine=SpeedAwareEngine(),
    )
    assert summary["speed_edges"] > 0
    edges = store.graph_edges(summary["article_id"])
    kinds = {e["kind"] for e in edges}
    assert "probes_sensemaking_speed" in kinds
    assert "exploits_speed_differential" in kinds and "processes_faster_than" in kinds
    assert store.summary()["speed_edge_count"] == len(edges)


def test_no_speed_edges_without_evidence(tmp_path) -> None:
    store = SliceStore(tmp_path)
    summary = ingest_and_assess(_ARTICLE, source_id="r", title="t", store=store)
    assert summary["speed_edges"] == 0 and store.graph_edges() == []


def test_gap_analysis_over_stored_corpus(tmp_path, capsys) -> None:
    """FR-ASSSIB-04: the runner consumes the explicit none_evident gap signals."""
    from hanani.gaps import analyze_gaps

    store = SliceStore(tmp_path)
    ingest_and_assess(_ARTICLE, source_id="reuters", title="Odesa", store=store)
    report = analyze_gaps(store)

    assert report["assessed"] > 0 and report["gated"] > 0
    # default engine records none_evident blocks → every assessed atom is a gap
    assert report["speed_gaps"] == report["assessed"]
    assert report["gap_rate"] == 1.0
    kinds = {f["kind"] for f in report["findings"]}
    assert "speed_gap" in kinds and "no_party_linkage" in kinds
    # FR-ASSSIB-05: gaps exist → retrieval priorities surface
    assert report["retrieval_priorities"]
    assert len(report["questions"]) >= 5

    # CLI renders it
    from hanani.cli import main
    assert main(["gaps", "--store", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "speed gaps:" in out and "retrieve next" in out


def test_gap_analysis_empty_store(tmp_path) -> None:
    from hanani.gaps import analyze_gaps

    report = analyze_gaps(SliceStore(tmp_path))
    assert report["assessed"] == 0 and report["findings"] == []
    assert report["retrieval_priorities"] == []  # no gaps → no retrieval push


def test_gap_analysis_no_gaps_when_speed_evidence_present(tmp_path) -> None:
    from hanani.gaps import analyze_gaps
    from hanani.reasoning import ReasoningEngine, SpeedDifferentialAssessment

    class SpeedAwareEngine(ReasoningEngine):
        def assess_atom(self, atom, **kwargs):
            kwargs["speed"] = SpeedDifferentialAssessment(
                side_a_processing="fast", side_b_processing="slow",
                side_a_party_id="ru", side_b_party_id="nato",
                probe_intent="measure_reaction_speed",
                differential_exploited="side_a_exploits", notes="observed",
            )
            return super().assess_atom(atom, **kwargs)

    store = SliceStore(tmp_path)
    ingest_and_assess(_ARTICLE, source_id="r", title="t", store=store,
                      engine=SpeedAwareEngine())
    report = analyze_gaps(store)
    assert report["speed_gaps"] == 0 and report["gap_rate"] == 0.0
    assert not any(f["kind"] == "no_party_linkage" for f in report["findings"])
