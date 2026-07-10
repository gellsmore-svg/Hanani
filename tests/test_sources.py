"""Tests for source corpus and article history (FR-SOURCE-04)."""

from __future__ import annotations

from datetime import datetime, timezone

from hanani.sources import SourceCorpus, content_hash


def test_content_hash_stable() -> None:
    assert content_hash("hello") == content_hash("hello")
    assert content_hash("hello") != content_hash("world")


def test_source_history_chronological() -> None:
    corpus = SourceCorpus()
    t1 = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
    t2 = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    t3 = datetime(2026, 7, 3, 12, 0, tzinfo=timezone.utc)

    corpus.register(source_id="src-a", title="First", text="body one", provenance="manual", ingested_at=t1)
    corpus.register(source_id="src-a", title="Third", text="body three", provenance="manual", ingested_at=t3)
    corpus.register(source_id="src-a", title="Second", text="body two", provenance="manual", ingested_at=t2)

    history = corpus.history("src-a")
    assert [a.title for a in history] == ["First", "Third", "Second"]
    assert len(corpus.all_sources()) == 1


def test_link_atoms_to_article() -> None:
    corpus = SourceCorpus()
    article = corpus.register(
        source_id="src-b",
        title="Probe report",
        text="Alliance coordination lag",
        provenance="ingest",
    )
    corpus.link_atoms(article.article_id, ["atom-1", "atom-2"])
    assert corpus.article(article.article_id).atom_ids == ["atom-1", "atom-2"]


def test_corpus_summary() -> None:
    corpus = SourceCorpus()
    corpus.register(source_id="s1", title="A", text="x", provenance="p")
    corpus.register(source_id="s2", title="B", text="y", provenance="p")
    summary = corpus.summary()
    assert summary["source_count"] == 2
    assert summary["article_count"] == 2