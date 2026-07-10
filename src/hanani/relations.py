"""Semantic relational mapping between logic atoms (FR-ANALYSIS-01).

Atoms stop being islands: this module maps assessed atoms into typed,
**auditable** relations drawn only from the registered vocabulary
(:data:`hanani.graph.ATOM_EDGE_TYPES`). Family pattern throughout:

* a **deterministic floor** that always runs offline — duplicates,
  same-article temporal sequence, and cross-source lexical corroboration
  candidates — every edge carrying ``basis="deterministic:<rule>"`` + score;
* an optional **model tier** (injectable ``ask``) proposing richer typed
  relations (contradicts / implies / supports / weakens), **validated against
  the vocabulary** — an invented edge type is dropped, never stored.

The Layer-1 gate is respected: only admissible atoms participate in
inferential relations; duplicates/sequence may include gated atoms (corpus
hygiene). Relations persist beside the ASSSIB speed edges in
``graph_edges.jsonl``.
"""

from __future__ import annotations

import json
import re
from itertools import combinations
from typing import Any, Callable

from hanani.graph import ATOM_EDGE_TYPES
from hanani.store import SliceStore

AskFn = Callable[[str], str]

_INFERENTIAL = frozenset({"contradicts", "implies", "supports", "weakens"})
_WORD_RE = re.compile(r"[a-z0-9]+")
_STOP = {
    "the", "and", "for", "with", "that", "this", "from", "have", "has", "are",
    "was", "were", "been", "its", "his", "her", "their", "a", "an", "of", "to",
    "in", "on", "as", "is", "it", "by", "or", "at", "not", "but", "will",
    "would", "since", "after", "before", "into", "over", "than",
}

_CORROBORATE_OVERLAP = 0.55
_COMPLEMENT_OVERLAP = 0.30


def _tokens(text: str) -> frozenset[str]:
    return frozenset(
        w for w in _WORD_RE.findall((text or "").lower())
        if len(w) >= 3 and w not in _STOP
    )


def _overlap(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _edge(source: str, target: str, kind: str, basis: str, score: float) -> dict[str, Any]:
    return {
        "source": source,
        "target": target,
        "kind": kind,
        "properties": {"basis": basis, "score": round(score, 3)},
    }


def _atom_view(record: dict[str, Any]) -> dict[str, Any]:
    atom = record.get("atom") or {}
    return {
        "atom_id": str(atom.get("atom_id", "?")),
        "source_id": str(atom.get("source_id", "?")),
        "text": str(atom.get("text", "")),
        "article_id": str(record.get("article_id", "")),
        "admissible": record.get("layer2") is not None,
        "tokens": _tokens(str(atom.get("text", ""))),
    }


def relate_atoms(
    assessments: list[dict[str, Any]], *, ask: AskFn | None = None
) -> list[dict[str, Any]]:
    """Typed atom→atom relations: deterministic floor + validated model tier."""
    views = [_atom_view(r) for r in assessments]
    seen_pairs: set[tuple[str, str]] = set()
    edges: list[dict[str, Any]] = []

    # temporal sequence within each article (corpus hygiene; gated atoms allowed)
    by_article: dict[str, list[dict[str, Any]]] = {}
    for view in views:
        by_article.setdefault(view["article_id"], []).append(view)
    for atoms in by_article.values():
        for earlier, later in zip(atoms, atoms[1:]):
            edges.append(_edge(earlier["atom_id"], later["atom_id"], "yields",
                               "deterministic:same_article_sequence", 1.0))

    for a, b in combinations(views, 2):
        pair = (a["atom_id"], b["atom_id"])
        if pair in seen_pairs or a["atom_id"] == b["atom_id"]:
            continue
        seen_pairs.add(pair)
        score = _overlap(a["tokens"], b["tokens"])
        if a["text"].strip().lower() == b["text"].strip().lower():
            edges.append(_edge(*pair, "agrees", "deterministic:duplicate_text", 1.0))
            continue
        if a["source_id"] != b["source_id"] and a["admissible"] and b["admissible"]:
            if score >= _CORROBORATE_OVERLAP:
                edges.append(_edge(*pair, "agrees",
                                   "deterministic:cross_source_overlap", score))
            elif score >= _COMPLEMENT_OVERLAP:
                edges.append(_edge(*pair, "complements",
                                   "deterministic:cross_source_overlap", score))

    if ask is not None:
        edges.extend(_model_relations(views, ask))
    return edges


def _model_relations(views: list[dict[str, Any]], ask: AskFn) -> list[dict[str, Any]]:
    """Model-proposed typed relations, vocabulary-validated, admissible-only."""
    admissible = [v for v in views if v["admissible"]]
    if len(admissible) < 2:
        return []
    catalogue = "\n".join(f"{v['atom_id']}: {v['text']}" for v in admissible[:25])
    prompt = (
        "Identify semantic relations between these logic atoms. Allowed kinds: "
        + ", ".join(sorted(_INFERENTIAL))
        + '. Return ONLY a JSON array of {"source": id, "target": id, "kind": kind}.'
        + f"\n\nATOMS:\n{catalogue}"
    )
    known = {v["atom_id"] for v in admissible}
    edges: list[dict[str, Any]] = []
    try:
        raw = ask(prompt)
        data = json.loads(raw[raw.index("[") : raw.rindex("]") + 1])
    except Exception:  # noqa: BLE001 - model tier is best-effort
        return []
    for item in data:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind", ""))
        source, target = str(item.get("source", "")), str(item.get("target", ""))
        if (
            kind in _INFERENTIAL
            and kind in ATOM_EDGE_TYPES
            and source in known
            and target in known
            and source != target
        ):
            edges.append(_edge(source, target, kind, "model", 0.5))
    return edges


def map_relations(
    store: SliceStore, *, article_id: str | None = None, ask: AskFn | None = None
) -> dict[str, Any]:
    """Relate the stored atoms (whole corpus or one article) and persist edges."""
    assessments = store.assessments(article_id)
    if article_id is not None and not assessments:
        raise ValueError(f"unknown article_id in store: {article_id}")
    edges = relate_atoms(assessments, ask=ask)
    store.save_graph_edges(article_id or "corpus-relations", edges)
    kinds: dict[str, int] = {}
    for edge in edges:
        kinds[edge["kind"]] = kinds.get(edge["kind"], 0) + 1
    return {
        "scope": article_id or "corpus",
        "atom_count": len(assessments),
        "relation_count": len(edges),
        "kinds": kinds,
        "model_tier": ask is not None,
    }
