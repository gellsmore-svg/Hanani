"""Hanani's MCP tool handlers — execute the manifest's capabilities.

The Keturah stdio MCP server only advertises tools it can dispatch, so each
handler here is registered under the exact (namespaced + short) name of a
manifest capability. Defensive: handler errors return ``{"error": …}`` rather
than raising into the calling agent.
"""

from __future__ import annotations

from typing import Any, Callable

from hanani.store import SliceStore


def build_handlers(*, store: SliceStore | None = None) -> dict[str, Callable[..., Any]]:
    """Hanani's MCP handlers keyed by tool name (namespaced + short)."""

    def _store() -> SliceStore:
        return store if store is not None else SliceStore()

    def ingest_and_assess(
        text: str = "",
        source_id: str = "",
        title: str = "",
        provenance: str = "mcp",
        max_atoms: int = 10,
        **_kw: Any,
    ) -> dict[str, Any]:
        from hanani.pipeline import ingest_and_assess as run_slice

        if not str(text).strip():
            return {"error": "text is required"}
        if not str(source_id).strip() or not str(title).strip():
            return {"error": "source_id and title are required"}
        try:
            return run_slice(
                text,
                source_id=source_id,
                title=title,
                provenance=provenance,
                store=_store(),
                max_atoms=max(1, min(int(max_atoms), 25)),
            )
        except Exception as exc:  # noqa: BLE001 - surface cleanly to the agent
            return {"error": f"ingest failed: {type(exc).__name__}: {exc}"}

    def corpus_summary(**_kw: Any) -> dict[str, Any]:
        try:
            return _store().summary()
        except Exception as exc:  # noqa: BLE001
            return {"error": f"summary failed: {type(exc).__name__}: {exc}"}

    def debate_corpus(
        article_id: str | None = None,
        max_iterations: int = 3,
        extractor: str = "rule",
        **_kw: Any,
    ) -> dict[str, Any]:
        from hanani.debate import debate_corpus as run_debate

        try:
            return run_debate(
                _store(),
                article_id=article_id,
                max_iterations=max_iterations,
                extractor=extractor if extractor in ("rule", "hoglah") else "rule",
            )
        except (RuntimeError, ValueError) as exc:
            return {"error": str(exc)}
        except Exception as exc:  # noqa: BLE001 - surface cleanly to the agent
            return {"error": f"debate failed: {type(exc).__name__}: {exc}"}

    def analyze_gaps(**_kw: Any) -> dict[str, Any]:
        from hanani.gaps import analyze_gaps as run_gaps

        try:
            return run_gaps(_store())
        except Exception as exc:  # noqa: BLE001
            return {"error": f"gap analysis failed: {type(exc).__name__}: {exc}"}

    def map_relations(article_id: str | None = None, **_kw: Any) -> dict[str, Any]:
        from hanani.relations import map_relations as run_relations

        try:
            return run_relations(_store(), article_id=article_id)
        except ValueError as exc:
            return {"error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            return {"error": f"relations failed: {type(exc).__name__}: {exc}"}

    def factors(**_kw: Any) -> dict[str, Any]:
        from hanani.factors import list_factors

        return {"factors": list_factors()}

    return {
        "hanani.ingest_and_assess": ingest_and_assess,
        "ingest_and_assess": ingest_and_assess,
        "hanani.corpus_summary": corpus_summary,
        "corpus_summary": corpus_summary,
        "hanani.debate_corpus": debate_corpus,
        "debate_corpus": debate_corpus,
        "hanani.analyze_gaps": analyze_gaps,
        "analyze_gaps": analyze_gaps,
        "hanani.map_relations": map_relations,
        "map_relations": map_relations,
        "hanani.factors": factors,
        "factors": factors,
    }
