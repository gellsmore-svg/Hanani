"""Tirzah push increment — render + push via an injectable ingest seam."""

from __future__ import annotations

import pytest

from hanani.pipeline import ingest_and_assess
from hanani.store import SliceStore
from hanani.tirzah_push import push_to_tirzah, render_article_markdown

_ARTICLE = (
    "Insurance premiums for Black Sea grain shipments have risen by roughly a "
    "third since strikes on port infrastructure resumed last month. "
    "The West now has only two options: escalate its support or watch the "
    "corridor close entirely."
)


def _stored(tmp_path) -> SliceStore:
    store = SliceStore(tmp_path)
    ingest_and_assess(_ARTICLE, source_id="reuters", title="Grain corridor", store=store)
    return store


def test_render_article_markdown_structure(tmp_path) -> None:
    store = _stored(tmp_path)
    article = store.articles()[0]
    md = render_article_markdown(article, store.assessments(article["article_id"]))
    assert md.startswith("# Grain corridor")
    assert f"- hanani_article_id: {article['article_id']}" in md
    assert "## Atom assessments" in md
    assert "### atom-" in md
    assert "- robustness:" in md
    # the false-dilemma sentence renders its hit and its gate outcome
    assert "fallacy.false_dilemma" in md
    assert "not admissible" in md


def test_push_all_and_idempotent_duplicates(tmp_path) -> None:
    store = _stored(tmp_path)
    calls: list[tuple[str, list[str]]] = []
    seen_hashes: set[str] = set()

    def fake_ingest(path, labels):
        content = path.read_text(encoding="utf-8")
        calls.append((path.name, labels))
        if content in seen_hashes:
            return {"ok": False, "reason": "duplicate_checksum", "existing_document_id": "doc-1"}
        seen_hashes.add(content)
        return {"ok": True, "document_id": "doc-1"}

    first = push_to_tirzah(store, ingest=fake_ingest)
    assert first["pushed"] == 1 and first["duplicates"] == 0 and first["failed"] == 0
    assert first["results"][0]["document_id"] == "doc-1"

    again = push_to_tirzah(store, ingest=fake_ingest)
    assert again["pushed"] == 0 and again["duplicates"] == 1 and again["failed"] == 0

    name, labels = calls[0]
    assert name.startswith("hanani-grain-corridor") and name.endswith(".md")
    assert "hanani" in labels and "hanani-source-reuters" in labels


def test_push_single_article_and_unknown_id(tmp_path) -> None:
    store = _stored(tmp_path)
    aid = store.articles()[0]["article_id"]
    summary = push_to_tirzah(store, article_id=aid, ingest=lambda p, labels: {"ok": True, "document_id": "d"})
    assert summary["pushed"] == 1
    with pytest.raises(ValueError, match="unknown article_id"):
        push_to_tirzah(store, article_id="nope", ingest=lambda p, labels: {"ok": True})


def test_push_survives_per_article_errors(tmp_path) -> None:
    store = _stored(tmp_path)
    ingest_and_assess(_ARTICLE + " More text here.", source_id="ap", title="Second", store=store)

    def flaky(path, labels):
        if "grain-corridor" in path.name:
            raise ConnectionError("mongo down")
        return {"ok": True, "document_id": "doc-2"}

    summary = push_to_tirzah(store, ingest=flaky)
    assert summary["pushed"] == 1 and summary["failed"] == 1
    errs = [r for r in summary["results"] if not r["ok"]]
    assert "mongo down" in errs[0]["error"]


def test_missing_extra_raises_clean_runtime_error(tmp_path, monkeypatch) -> None:
    import hanani.tirzah_push as tp

    def boom(_cfg):
        raise ImportError("No module named 'tirzah'")

    monkeypatch.setattr(tp, "_default_ingest", boom)
    with pytest.raises(RuntimeError, match="tirzah extra"):
        push_to_tirzah(_stored(tmp_path))
