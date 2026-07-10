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
                "debate_corpus",
                "Milcah multi-LLM debate over the Layer-1-admissible atoms "
                "(one article or the whole store): pressure-tests what the "
                "combined reports imply, returning a bounded verdict — claims, "
                "objections, evidence, confidence, terminal_reason. Gated "
                "(inadmissible) atoms are excluded and listed.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "article_id": {"type": "string", "description": "debate one article (omit for whole corpus)"},
                        "max_iterations": {"type": "integer", "minimum": 1, "maximum": 10, "default": 3},
                        "extractor": {"type": "string", "enum": ["rule", "hoglah"], "default": "rule"},
                    },
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "scope": {"type": "string"},
                        "debated_atom_ids": {"type": "array", "items": {"type": "string"}},
                        "excluded_inadmissible": {"type": "array", "items": {"type": "string"}},
                        "verdict": {"type": "object"},
                    },
                },
                tags=["reasoning", "debate", "milcah"],
            ),
            capability(
                "analyze_gaps",
                "ASSSIB gap analysis over the persisted corpus: which assessed "
                "atoms carry explicit none_evident speed blocks, which flagged "
                "sensemaking signals without speed evidence, party-linkage "
                "coverage — with the normative gap questions and, when gaps "
                "exist, the retrieval priorities (FR-ASSSIB-04/05).",
                input_schema={"type": "object", "properties": {}},
                output_schema={
                    "type": "object",
                    "properties": {
                        "assessed": {"type": "integer"},
                        "speed_gaps": {"type": "integer"},
                        "gap_rate": {"type": "number"},
                        "findings": {"type": "array", "items": {"type": "object"}},
                        "retrieval_priorities": {"type": "array", "items": {"type": "string"}},
                    },
                },
                tags=["reasoning", "gaps", "asssib"],
            ),
            capability(
                "map_relations",
                "Semantic relational mapping between logic atoms: typed, "
                "auditable edges (agrees/complements/yields from the "
                "deterministic floor; contradicts/implies/supports/weakens via "
                "the validated model tier), persisted to the analysis graph "
                "(FR-ANALYSIS-01).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "article_id": {"type": "string", "description": "relate one article (omit for whole corpus)"},
                    },
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "scope": {"type": "string"},
                        "atom_count": {"type": "integer"},
                        "relation_count": {"type": "integer"},
                        "kinds": {"type": "object"},
                    },
                },
                tags=["reasoning", "graph", "relations"],
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
