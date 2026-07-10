"""Milcah debate increment — admissible atoms only, injectable runner."""

from __future__ import annotations

import pytest

from hanani.debate import GUIDING_QUESTION, build_debate_input, debate_corpus
from hanani.pipeline import ingest_and_assess
from hanani.store import SliceStore

_ARTICLE = (
    "Insurance premiums for Black Sea grain shipments have risen by roughly a "
    "third since strikes on port infrastructure resumed last month. "
    "Grain transit volumes through the corridor fell fifteen percent in June. "
    "The West now has only two options: escalate its support or watch the "
    "corridor close entirely."
)


def _stored(tmp_path) -> SliceStore:
    store = SliceStore(tmp_path)
    ingest_and_assess(_ARTICLE, source_id="reuters", title="Grain corridor", store=store)
    return store


def test_build_debate_input_excludes_gated_atoms(tmp_path) -> None:
    store = _stored(tmp_path)
    query, context, debated, excluded = build_debate_input(store.assessments())
    assert query == GUIDING_QUESTION
    assert debated and excluded, "expected both admissible and gated atoms"
    assert "only two options" not in context  # the false-dilemma atom is gated out
    assert "[reuters | Strong]" in context
    assert set(debated).isdisjoint(set(excluded))


def test_debate_corpus_persists_verdict(tmp_path) -> None:
    store = _stored(tmp_path)
    seen: dict = {}

    def fake_run(request):
        seen.update(request)
        return {
            "claims": ["premium rises and volume falls are mutually coherent"],
            "objections": ["no direct evidence links the strikes to the premium change"],
            "evidence": ["atoms 1-2"], "citations": [],
            "confidence": 0.55, "terminal_reason": "converged",
        }

    record = debate_corpus(store, run=fake_run)
    assert seen["mode"] == "coherence" and seen["query"] == GUIDING_QUESTION
    assert "COMBINED CLAIM SET" in seen["context"]
    assert record["scope"] == "corpus"
    assert record["verdict"]["confidence"] == 0.55
    assert record["excluded_inadmissible"]

    stored = store.debates()
    assert len(stored) == 1 and stored[0]["verdict"]["terminal_reason"] == "converged"
    assert store.summary()["debate_count"] == 1


def test_debate_normalises_object_results(tmp_path) -> None:
    store = _stored(tmp_path)

    class ObjResult:
        claims = ["c"]
        objections = []
        evidence = []
        citations = []
        confidence = 0.8
        terminal_reason = "no_objections"

    record = debate_corpus(store, run=lambda _r: ObjResult())
    assert record["verdict"]["claims"] == ["c"]
    assert record["verdict"]["terminal_reason"] == "no_objections"
    # blocked verdicts keep their reason auditable
    blocked = debate_corpus(
        store, run=lambda _r: {"terminal_reason": "blocked", "error": "job timeout",
                               "error_type": "TimeoutError"},
    )
    assert blocked["verdict"]["error"] == "job timeout"
    assert blocked["verdict"]["error_type"] == "TimeoutError"


def test_debate_single_article_and_errors(tmp_path) -> None:
    store = _stored(tmp_path)
    aid = store.articles()[0]["article_id"]
    record = debate_corpus(store, article_id=aid, run=lambda _r: {"confidence": 0.1})
    assert record["article_id"] == aid and record["scope"] == aid

    with pytest.raises(ValueError, match="unknown article_id"):
        debate_corpus(store, article_id="nope", run=lambda _r: {})

    empty = SliceStore(tmp_path / "empty")
    with pytest.raises(ValueError, match="no admissible atoms"):
        debate_corpus(empty, run=lambda _r: {})


def test_missing_milcah_extra_raises_cleanly(tmp_path, monkeypatch) -> None:
    import hanani.debate as dbt

    def boom(_extractor):
        raise ImportError("No module named 'milcah'")

    monkeypatch.setattr(dbt, "_milcah_run", boom)
    with pytest.raises(RuntimeError, match="milcah extra"):
        debate_corpus(_stored(tmp_path))


def test_mcp_debate_handler_reports_errors(tmp_path) -> None:
    from hanani.mcp_handlers import build_handlers

    handlers = build_handlers(store=SliceStore(tmp_path / "empty"))
    out = handlers["hanani.debate_corpus"]()
    assert "error" in out  # empty store (or missing milcah) surfaces cleanly
