"""Local persistence for the vertical slice — articles and atom assessments.

Dependency-free JSONL under ``~/.hanani`` (directory overridable): one line per
record, append-only, tolerant of unreadable lines. This is the slice's honest
persistence floor; pushing the same records into Tirzah's graph memory is a
later increment behind the ``tirzah`` extra.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_STORE_DIR = Path.home() / ".hanani"


class SliceStore:
    """Append-only JSONL store for witness articles and atom assessments."""

    def __init__(self, directory: str | Path = DEFAULT_STORE_DIR) -> None:
        self.directory = Path(directory)
        self.articles_path = self.directory / "articles.jsonl"
        self.assessments_path = self.directory / "assessments.jsonl"
        self.debates_path = self.directory / "debates.jsonl"
        self.graph_edges_path = self.directory / "graph_edges.jsonl"

    def _append(self, path: Path, record: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    @staticmethod
    def _load(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                records.append(record)
        return records

    # --- write ---------------------------------------------------------

    def save_article(self, article: dict[str, Any]) -> None:
        self._append(self.articles_path, article)

    def save_assessments(self, article_id: str, records: list[dict[str, Any]]) -> None:
        for record in records:
            self._append(self.assessments_path, {"article_id": article_id, **record})

    def save_debate(self, record: dict[str, Any]) -> None:
        self._append(self.debates_path, record)

    def save_graph_edges(self, article_id: str, edges: list[dict[str, Any]]) -> None:
        for edge in edges:
            self._append(self.graph_edges_path, {"article_id": article_id, **edge})

    # --- read ----------------------------------------------------------

    def articles(self) -> list[dict[str, Any]]:
        return self._load(self.articles_path)

    def assessments(self, article_id: str | None = None) -> list[dict[str, Any]]:
        records = self._load(self.assessments_path)
        if article_id is None:
            return records
        return [r for r in records if r.get("article_id") == article_id]

    def graph_edges(self, article_id: str | None = None) -> list[dict[str, Any]]:
        records = self._load(self.graph_edges_path)
        if article_id is None:
            return records
        return [r for r in records if r.get("article_id") == article_id]

    def debates(self, article_id: str | None = None) -> list[dict[str, Any]]:
        records = self._load(self.debates_path)
        if article_id is None:
            return records
        return [r for r in records if r.get("article_id") == article_id]

    def summary(self) -> dict[str, Any]:
        articles = self.articles()
        assessments = self.assessments()
        robustness: dict[str, int] = {}
        admissible = 0
        for record in assessments:
            layer1 = record.get("layer1") or {}
            tier = str(layer1.get("robustness") or "unknown")
            robustness[tier] = robustness.get(tier, 0) + 1
            if record.get("layer2") is not None:
                admissible += 1
        return {
            "store_dir": str(self.directory),
            "article_count": len(articles),
            "atom_count": len(assessments),
            "admissible_atoms": admissible,
            "robustness": robustness,
            "sources": sorted({a.get("source_id", "?") for a in articles}),
            "debate_count": len(self.debates()),
            "speed_edge_count": len(self.graph_edges()),
        }
