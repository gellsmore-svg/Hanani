"""CLI for Hanani — Geopolitical News Reasoning."""

from __future__ import annotations

import argparse
import sys

from hanani import __version__
from hanani.factors import list_factors
from hanani.ontology import ONTOLOGY_DOC, ONTOLOGY_VERSION, list_layers
from hanani.reasoning import REASONING_VERSION, default_engine
from hanani.rhetoric import RHETORIC_GRAPH_VERSION, list_fallacies
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

    docs = sub.add_parser("docs", help="Documentation site (build / serve)")
    docs_sub = docs.add_subparsers(dest="docs_command")
    docs_sub.add_parser("build", help="Build docs/web from Markdown")
    docs_sub.add_parser("serve", help="Build and serve docs at http://127.0.0.1:8765")

    workflow = sub.add_parser("workflow", help="Workflow orchestration")
    workflow_sub = workflow.add_subparsers(dest="workflow_command")
    workflow_sub.add_parser("status", help="Workflow status").set_defaults(
        func=_cmd_workflow_status
    )

    args = parser.parse_args(argv)
    if not args.command:
        print(PURPOSE)
        print("Try: hanani reasoning | hanani ontology | hanani rhetoric | hanani factors")
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