"""Keturah capability manifest for Hanani — the LLM-callable interfaces.

``build_manifest()`` is the federation seam: Tirzah's ``family_registry()``
aggregates it (fail-soft) so Hanani's tools appear in the family capability
view and, with handlers wired, in the Keturah MCP server's ``tools/list``.
"""

from __future__ import annotations

from hanani import __version__


def build_manifest():
    """Hanani's capability manifest (requires keturah)."""
    from keturah import capability, manifest

    return manifest(
        "hanani",
        version=__version__,
        description="Geopolitical news reasoning: article → logic atoms → "
        "Layer 1 rhetoric audit → Layer 2 mechanism assessment, persisted.",
        capabilities=[
            capability(
                "ingest_and_assess",
                "Run the reasoning slice on one article: extract claim atoms, "
                "audit each against the rhetoric/fallacy graph (Layer 1), gate "
                "inadmissible atoms, assess mechanisms (Layer 2), and persist. "
                "Returns the article id, atom count, per-tier robustness, and "
                "how many atoms passed the admissibility gate.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "the article text"},
                        "source_id": {"type": "string", "description": "analytical source id (e.g. reuters)"},
                        "title": {"type": "string"},
                        "provenance": {"type": "string", "default": "mcp"},
                        "max_atoms": {"type": "integer", "minimum": 1, "maximum": 25, "default": 10},
                    },
                    "required": ["text", "source_id", "title"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "article_id": {"type": "string"},
                        "atom_count": {"type": "integer"},
                        "admissible_atoms": {"type": "integer"},
                        "robustness": {"type": "object"},
                    },
                },
                tags=["reasoning", "ingest", "geopolitics"],
            ),
            capability(
                "corpus_summary",
                "Summarise Hanani's persisted slice store: articles, atoms, "
                "admissible counts, robustness tiers, and sources.",
                input_schema={"type": "object", "properties": {}},
                output_schema={
                    "type": "object",
                    "properties": {
                        "article_count": {"type": "integer"},
                        "atom_count": {"type": "integer"},
                        "admissible_atoms": {"type": "integer"},
                        "robustness": {"type": "object"},
                        "sources": {"type": "array", "items": {"type": "string"}},
                    },
                },
                tags=["corpus", "status"],
            ),
            capability(
                "factors",
                "List the geopolitical factor taxonomy.",
                input_schema={"type": "object", "properties": {}},
                tags=["taxonomy"],
            ),
        ],
    )


def capabilities() -> dict:
    """Back-compat dict view (fail-soft when keturah is absent)."""
    try:
        return build_manifest().to_dict()
    except ImportError:
        return {
            "product": "hanani",
            "version": __version__,
            "capabilities": [],
            "note": "Install keturah for full manifest schema.",
        }
