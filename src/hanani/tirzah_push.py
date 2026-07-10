"""Push persisted slice records into Tirzah's graph memory (``tirzah`` extra).

Each stored article (plus its atom assessments) is rendered as a structured
markdown document and ingested through Tirzah's **supported** document pipeline
(``ingest_source_path``): checksum dedup, parsing into source_root/section/chunk
nodes, and embeddings. Riding that path — rather than writing raw nodes — keeps
Hanani's records searchable like any other Tirzah memory, and makes re-pushes
idempotent (identical content is rejected as ``duplicate_checksum``).

Everything is injectable for tests; the real Tirzah/Mongo chain is only built
when no ``ingest`` callable is supplied.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any, Callable

from hanani.store import SliceStore

IngestFn = Callable[[Path, list[str]], dict[str, Any]]

_SLUG_RE = re.compile(r"[^a-z0-9-]+")


def _slug(text: str) -> str:
    slug = _SLUG_RE.sub("-", (text or "").lower()).strip("-")
    return slug[:60] or "article"


def render_article_markdown(article: dict[str, Any], assessments: list[dict[str, Any]]) -> str:
    """One article + its atom assessments as a Tirzah-ingestable markdown doc."""
    title = article.get("title") or article.get("article_id") or "Untitled"
    lines = [
        f"# {title}",
        "",
        f"- hanani_article_id: {article.get('article_id')}",
        f"- source_id: {article.get('source_id')}",
        f"- ingested_at: {article.get('ingested_at')}",
        f"- provenance: {article.get('provenance')}",
        f"- content_hash: {article.get('content_hash')}",
        "",
        "## Atom assessments",
        "",
    ]
    for record in assessments:
        atom = record.get("atom") or {}
        layer1 = record.get("layer1") or {}
        layer2 = record.get("layer2")
        lines.append(f"### {atom.get('atom_id', 'atom')}")
        lines.append("")
        lines.append(str(atom.get("text", "")).strip())
        lines.append("")
        lines.append(f"- robustness: {layer1.get('robustness', 'unknown')}")
        hits = list(layer1.get("fallacy_hits") or []) + list(layer1.get("enthymeme_hits") or [])
        if hits:
            lines.append(f"- rhetoric_hits: {', '.join(hits)}")
        if layer2 is None:
            lines.append("- layer2: not admissible (failed the Layer 1 gate)")
        else:
            tags = layer2.get("tags") or []
            lines.append(f"- layer2_tags: {', '.join(tags) if tags else '(none)'}")
        lines.append("")
    return "\n".join(lines)


def _default_ingest(config_path: str | None) -> IngestFn:
    """The real chain: Tirzah config + Mongo + the supported document pipeline."""
    from tirzah.cli import ingest_source_path
    from tirzah.config import load_config
    from tirzah.db.client import get_database

    config = load_config(config_path) if config_path else load_config()
    db = get_database(config.mongo)

    def ingest(path: Path, labels: list[str]) -> dict[str, Any]:
        return ingest_source_path(db, config, path, labels)

    return ingest


def push_to_tirzah(
    store: SliceStore,
    *,
    article_id: str | None = None,
    labels: tuple[str, ...] = ("hanani",),
    config_path: str | None = None,
    ingest: IngestFn | None = None,
) -> dict[str, Any]:
    """Push stored slice records into Tirzah memory. Idempotent by checksum.

    Returns ``{pushed, duplicates, failed, results}`` where each result carries
    the article id and Tirzah's ingest outcome (document id, or the duplicate/
    error reason).
    """
    if ingest is None:
        try:
            ingest = _default_ingest(config_path)
        except Exception as error:  # noqa: BLE001 - the extra may be missing
            raise RuntimeError(
                "tirzah push needs the tirzah extra and a reachable Tirzah config/Mongo "
                f"(pip install 'hanani[tirzah]'): {error}"
            ) from error

    articles = store.articles()
    if article_id is not None:
        articles = [a for a in articles if a.get("article_id") == article_id]
        if not articles:
            raise ValueError(f"unknown article_id in store: {article_id}")

    pushed = duplicates = failed = 0
    results: list[dict[str, Any]] = []
    for article in articles:
        aid = str(article.get("article_id"))
        markdown = render_article_markdown(article, store.assessments(aid))
        article_labels = [*labels, f"hanani-source-{article.get('source_id', 'unknown')}"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f"hanani-{_slug(str(article.get('title') or aid))}.md"
            path.write_text(markdown, encoding="utf-8")
            try:
                outcome = ingest(path, article_labels)
            except Exception as error:  # noqa: BLE001 - keep pushing the rest
                failed += 1
                results.append({"article_id": aid, "ok": False, "error": str(error)})
                continue
        if outcome.get("ok"):
            pushed += 1
        elif outcome.get("reason") == "duplicate_checksum":
            duplicates += 1
        else:
            failed += 1
        results.append(
            {
                "article_id": aid,
                "ok": bool(outcome.get("ok")),
                "document_id": outcome.get("document_id") or outcome.get("existing_document_id"),
                "reason": outcome.get("reason"),
            }
        )
    return {"pushed": pushed, "duplicates": duplicates, "failed": failed, "results": results}
