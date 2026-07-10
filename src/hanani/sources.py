"""Source corpus — witness registry and per-source article history."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def content_hash(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


@dataclass
class WitnessArticle:
    """One ingested article (witness) in temporal sequence for a source."""

    article_id: str
    source_id: str
    title: str
    ingested_at: datetime
    content_hash: str
    provenance: str
    atom_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ingested_at"] = self.ingested_at.isoformat()
        return data


@dataclass
class SourceCorpus:
    """Temporal article history per analytical source (reputation-blind)."""

    articles: dict[str, WitnessArticle] = field(default_factory=dict)
    _by_source: dict[str, list[str]] = field(default_factory=dict)

    def register(
        self,
        *,
        source_id: str,
        title: str,
        text: str,
        provenance: str,
        article_id: str | None = None,
        ingested_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> WitnessArticle:
        """Register a witness article; append to source history in time order."""
        ts = ingested_at or _utc_now()
        aid = article_id or f"{source_id}-{content_hash(text)[:12]}"
        if aid in self.articles:
            raise ValueError(f"article_id already registered: {aid}")

        article = WitnessArticle(
            article_id=aid,
            source_id=source_id,
            title=title,
            ingested_at=ts,
            content_hash=content_hash(text),
            provenance=provenance,
            metadata=dict(metadata or {}),
        )
        self.articles[aid] = article
        self._by_source.setdefault(source_id, []).append(aid)
        self._sort_source(source_id)
        return article

    def link_atoms(self, article_id: str, atom_ids: list[str]) -> None:
        article = self._require(article_id)
        for atom_id in atom_ids:
            if atom_id not in article.atom_ids:
                article.atom_ids.append(atom_id)

    def history(self, source_id: str) -> list[WitnessArticle]:
        """Chronological article sequence for one source."""
        ids = self._by_source.get(source_id, [])
        return [self.articles[i] for i in ids]

    def all_sources(self) -> list[str]:
        return sorted(self._by_source.keys())

    def article(self, article_id: str) -> WitnessArticle:
        return self._require(article_id)

    def summary(self) -> dict[str, Any]:
        return {
            "source_count": len(self._by_source),
            "article_count": len(self.articles),
            "sources": {
                sid: {
                    "article_count": len(ids),
                    "first_ingested": self.articles[ids[0]].ingested_at.isoformat() if ids else None,
                    "last_ingested": self.articles[ids[-1]].ingested_at.isoformat() if ids else None,
                }
                for sid, ids in sorted(self._by_source.items())
            },
        }

    def _require(self, article_id: str) -> WitnessArticle:
        if article_id not in self.articles:
            raise KeyError(f"unknown article_id: {article_id}")
        return self.articles[article_id]

    def _sort_source(self, source_id: str) -> None:
        ids = self._by_source[source_id]
        ids.sort(key=lambda i: self.articles[i].ingested_at)


def default_corpus() -> SourceCorpus:
    return SourceCorpus()


__all__ = [
    "SourceCorpus",
    "WitnessArticle",
    "content_hash",
    "default_corpus",
]