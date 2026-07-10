"""CLI for Hanani — Geopolitical News Reasoning."""

from __future__ import annotations

import argparse
import sys

from hanani import __version__
from hanani.factors import list_factors
from hanani.ontology import ONTOLOGY_DOC, ONTOLOGY_VERSION, list_layers
from hanani.reasoning import REASONING_VERSION, default_engine
from hanani.rhetoric import RHETORIC_GRAPH_VERSION, list_fallacies
from hanani.assib import readiness
from hanani.coherence import default_registry
from hanani.sources import default_corpus
from hanani.workflow import workflow_status

PURPOSE = (
    "Hanani — Geopolitical News Reasoning.\n"
    "Evidence synthesis from multiple reports. Guiding question:\n"
    "  'What do all available reports imply when combined?'\n"
)


def _cmd_factors(_: argparse.Namespace) -> int:
    for factor in list_factors():
        print(f"  {factor['id']:30s}  {factor['label']}")
    return 0


def _cmd_reasoning(_: argparse.Namespace) -> int:
    engine = default_engine()
    summary = engine.registry_summary()
    print(f"reasoning engine: {REASONING_VERSION}")
    print(f"  rhetoric graph: {summary['rhetoric_graph_version']}")
    print(f"  fallacy patterns: {summary['fallacy_pattern_count']}")
    print(f"  mechanism layers: {len(summary['mechanism_layers'])}")
    print(f"  audit criteria: {summary['audit_criteria_count']}")
    print("  pipeline: Layer 1 rhetoric → Layer 2 mechanisms → [summary] → [narrative]")
    return 0


def _cmd_rhetoric(_: argparse.Namespace) -> int:
    print(f"rhetoric graph version: {RHETORIC_GRAPH_VERSION}")
    print(f"fallacy patterns: {len(list_fallacies())}")
    return 0


def _cmd_ontology(_: argparse.Namespace) -> int:
    print(f"mechanism graph version: {ONTOLOGY_VERSION}")
    print(f"document: {ONTOLOGY_DOC}")
    for layer, tags in list_layers().items():
        print(f"\n{layer}")
        for tag in tags:
            print(f"  - {tag}")
    return 0


def _cmd_workflow_status(_: argparse.Namespace) -> int:
    print(workflow_status())
    return 0


def _cmd_sources(_: argparse.Namespace) -> int:
    corpus = default_corpus()
    summary = corpus.summary()
    print(f"source corpus: {summary['source_count']} sources, {summary['article_count']} articles")
    for sid, info in summary["sources"].items():
        print(f"  {sid}: {info['article_count']} articles")
    return 0


def _cmd_asssib(_: argparse.Namespace) -> int:
    info = readiness()
    print(f"ASSSIB readiness: {info['ready']}")
    print(f"  dynamic: {info['dynamic']}")
    print(f"  mandatory per-atom speed_differential: {info['mandatory_per_atom']}")
    print(f"  coherence profiles: {info['coherence_profiles']}")
    print(f"  collective LCD: {info['collective_lcd']}")
    print(info["message"])
    return 0


def _cmd_coherence(_: argparse.Namespace) -> int:
    registry = default_registry()
    summary = registry.summary()
    print(f"coherence registry: {summary['individual_count']} parties, {summary['collective_count']} collectives")
    for cid, info in summary["collectives"].items():
        print(
            f"  {cid}: lcd_speed={info['lcd_reaction_speed']} "
            f"(member={info['lcd_speed_member']}), "
            f"lcd_coherence={info['lcd_coherence']} "
            f"(member={info['lcd_coherence_member']})"
        )
    return 0


def _cmd_ingest(args: argparse.Namespace) -> int:
    from pathlib import Path

    from hanani.pipeline import hoglah_ask, ingest_and_assess
    from hanani.store import SliceStore

    text = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
    ask = None
    if args.hoglah_model:
        ask = hoglah_ask(args.hoglah_model)
        if ask is None:
            print("warn: hoglah not installed — running the deterministic floor only", file=sys.stderr)
    try:
        summary = ingest_and_assess(
            text,
            source_id=args.source_id,
            title=args.title or Path(args.path).stem,
            provenance=args.provenance,
            ask=ask,
            store=SliceStore(args.store),
            max_atoms=args.max_atoms,
        )
    except ValueError as error:
        print(f"hanani ingest: {error}", file=sys.stderr)
        return 2
    print(f"article: {summary['article_id']}  ({summary['source_id']}: {summary['title']})")
    print(f"  atoms: {summary['atom_count']}  admissible→Layer2: {summary['admissible_atoms']}")
    print(f"  robustness: {summary['robustness']}")
    print(f"  model tier: {'on' if summary['model_tier'] else 'off (deterministic floor)'}")
    print(f"  stored: {summary['store_dir']}")
    return 0


def _cmd_push_tirzah(args: argparse.Namespace) -> int:
    from hanani.store import SliceStore
    from hanani.tirzah_push import push_to_tirzah

    try:
        summary = push_to_tirzah(
            SliceStore(args.store),
            article_id=args.article_id,
            config_path=args.config,
        )
    except (RuntimeError, ValueError) as error:
        print(f"hanani push-tirzah: {error}", file=sys.stderr)
        return 2
    print(
        f"tirzah push: {summary['pushed']} pushed, "
        f"{summary['duplicates']} duplicates, {summary['failed']} failed"
    )
    for result in summary["results"]:
        marker = "ok " if result["ok"] else ("dup" if result.get("reason") == "duplicate_checksum" else "ERR")
        print(f"  [{marker}] {result['article_id']} -> {result.get('document_id') or result.get('reason') or result.get('error')}")
    return 0 if summary["failed"] == 0 else 1


def _cmd_debate(args: argparse.Namespace) -> int:
    from hanani.debate import debate_corpus
    from hanani.store import SliceStore

    try:
        record = debate_corpus(
            SliceStore(args.store),
            article_id=args.article_id,
            max_iterations=args.max_iterations,
            extractor=args.extractor,
        )
    except (RuntimeError, ValueError) as error:
        print(f"hanani debate: {error}", file=sys.stderr)
        return 2
    verdict = record["verdict"]
    print(f"debate: scope={record['scope']}  atoms={len(record['debated_atom_ids'])} "
          f"(excluded inadmissible: {len(record['excluded_inadmissible'])})")
    print(f"  terminal: {verdict['terminal_reason']}  confidence: {verdict['confidence']:.2f}")
    for claim in verdict["claims"][:5]:
        print(f"  claim: {claim}")
    for objection in verdict["objections"][:5]:
        print(f"  objection: {objection}")
    if not verdict["objections"]:
        print("  objections: (none)")
    return 0


def _cmd_relations(args: argparse.Namespace) -> int:
    from hanani.relations import map_relations
    from hanani.store import SliceStore

    try:
        report = map_relations(SliceStore(args.store), article_id=args.article_id)
    except ValueError as error:
        print(f"hanani relations: {error}", file=sys.stderr)
        return 2
    print(f"relations: scope={report['scope']}  atoms={report['atom_count']}  "
          f"edges={report['relation_count']}")
    for kind, count in sorted(report["kinds"].items()):
        print(f"  {kind}: {count}")
    if not report["kinds"]:
        print("  (no relations found)")
    return 0


def _cmd_gaps(args: argparse.Namespace) -> int:
    from hanani.gaps import analyze_gaps
    from hanani.store import SliceStore

    report = analyze_gaps(SliceStore(args.store))
    print(f"gap analysis: {report['assessed']} assessed atoms "
          f"({report['gated']} rhetoric-gated) — speed gaps: {report['speed_gaps']} "
          f"(rate {report['gap_rate']:.0%})")
    for finding in report["findings"]:
        print(f"  [{finding['kind']}] {finding['note']}")
    if not report["findings"]:
        print("  no ASSSIB gaps above threshold")
    if report["retrieval_priorities"]:
        print("  retrieve next (FR-ASSSIB-05, Layer-1 filter applies):")
        for priority in report["retrieval_priorities"][:5]:
            print(f"    - {priority}")
    return 0


def _cmd_corpus(args: argparse.Namespace) -> int:
    from hanani.store import SliceStore

    summary = SliceStore(args.store).summary()
    print(f"stored corpus: {summary['article_count']} articles, {summary['atom_count']} atoms")
    print(f"  admissible atoms: {summary['admissible_atoms']}")
    print(f"  robustness: {summary['robustness']}")
    print(f"  sources: {', '.join(summary['sources']) or '(none)'}")
    print(f"  debates: {summary['debate_count']}")
    print(f"  graph edges: {summary['graph_edge_count']}")
    print(f"  store: {summary['store_dir']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hanani", description=PURPOSE)
    parser.add_argument("--version", action="version", version=f"hanani {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("factors", help="List factor taxonomy").set_defaults(func=_cmd_factors)
    sub.add_parser("ontology", help="Mechanism graph (version + layer tags)").set_defaults(
        func=_cmd_ontology
    )
    sub.add_parser("rhetoric", help="Rhetoric graph (fallacy pattern count)").set_defaults(
        func=_cmd_rhetoric
    )
    sub.add_parser("reasoning", help="Reasoning engine status").set_defaults(func=_cmd_reasoning)
    sub.add_parser("asssib", help="ASSSIB augmentation readiness").set_defaults(func=_cmd_asssib)
    sub.add_parser("sources", help="Source corpus status (article history)").set_defaults(func=_cmd_sources)
    sub.add_parser("coherence", help="Coherence speed profiles (individual + collective LCD)").set_defaults(
        func=_cmd_coherence
    )

    ingest = sub.add_parser(
        "ingest", help="Vertical slice: article → atoms → Layer 1 → Layer 2 → persist"
    )
    ingest.add_argument("path", help="Article text file, or '-' for stdin")
    ingest.add_argument("--source-id", required=True, help="Analytical source id (e.g. reuters)")
    ingest.add_argument("--title", default=None, help="Article title (default: file stem)")
    ingest.add_argument("--provenance", default="file", help="Where the text came from")
    ingest.add_argument("--max-atoms", type=int, default=10)
    ingest.add_argument("--hoglah-model", default=None,
                        help="Enable the model tier via the Hoglah queue (needs a running worker)")
    from hanani.store import DEFAULT_STORE_DIR

    ingest.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    ingest.set_defaults(func=_cmd_ingest)

    corpus_p = sub.add_parser("corpus", help="Summarise the persisted slice store")
    corpus_p.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    corpus_p.set_defaults(func=_cmd_corpus)

    debate_p = sub.add_parser(
        "debate", help="Milcah multi-LLM debate over the admissible atoms (milcah extra)"
    )
    debate_p.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    debate_p.add_argument("--article-id", default=None, help="Debate one article (default: whole corpus)")
    debate_p.add_argument("--max-iterations", type=int, default=3)
    debate_p.add_argument("--extractor", choices=("rule", "hoglah"), default="rule",
                          help="Milcah unit extraction: deterministic rule floor or the hoglah LLM tier")
    debate_p.set_defaults(func=_cmd_debate)

    rel_p = sub.add_parser("relations", help="Semantic relational mapping between atoms (FR-ANALYSIS-01)")
    rel_p.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    rel_p.add_argument("--article-id", default=None, help="Relate one article (default: whole corpus)")
    rel_p.set_defaults(func=_cmd_relations)

    gaps_p = sub.add_parser("gaps", help="ASSSIB gap analysis over the persisted corpus (FR-ASSSIB-04)")
    gaps_p.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    gaps_p.set_defaults(func=_cmd_gaps)

    push_p = sub.add_parser(
        "push-tirzah", help="Push stored articles+assessments into Tirzah memory (tirzah extra)"
    )
    push_p.add_argument("--store", default=str(DEFAULT_STORE_DIR), help="Store directory")
    push_p.add_argument("--article-id", default=None, help="Push one article (default: all)")
    push_p.add_argument("--config", default=None, help="Tirzah config.yaml path")
    push_p.set_defaults(func=_cmd_push_tirzah)

    docs = sub.add_parser("docs", help="Documentation site (build / serve)")
    docs_sub = docs.add_subparsers(dest="docs_command")
    docs_sub.add_parser("build", help="Build docs/web from Markdown")
    docs_sub.add_parser("serve", help="Build and serve docs at http://127.0.0.1:8805")

    workflow = sub.add_parser("workflow", help="Workflow orchestration")
    workflow_sub = workflow.add_subparsers(dest="workflow_command")
    workflow_sub.add_parser("status", help="Workflow status").set_defaults(
        func=_cmd_workflow_status
    )

    args = parser.parse_args(argv)
    if not args.command:
        print(PURPOSE)
        print(
            "Try: hanani reasoning | hanani asssib | hanani ontology | hanani sources | hanani coherence"
        )
        return 0

    if args.command == "workflow" and not getattr(args, "workflow_command", None):
        print(workflow_status())
        return 0

    if args.command == "docs":
        from hanani.docs_server import build_docs, serve

        if getattr(args, "docs_command", None) == "build":
            return build_docs()
        return serve()

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())