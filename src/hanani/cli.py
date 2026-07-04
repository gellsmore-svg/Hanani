"""CLI for Hanani — Geopolitical News Reasoning."""

from __future__ import annotations

import argparse
import sys

from hanani import __version__
from hanani.factors import list_factors
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


def _cmd_workflow_status(_: argparse.Namespace) -> int:
    print(workflow_status())
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hanani", description=PURPOSE)
    parser.add_argument("--version", action="version", version=f"hanani {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("factors", help="List factor taxonomy").set_defaults(func=_cmd_factors)

    workflow = sub.add_parser("workflow", help="Workflow orchestration")
    workflow_sub = workflow.add_subparsers(dest="workflow_command")
    workflow_sub.add_parser("status", help="Workflow status").set_defaults(
        func=_cmd_workflow_status
    )

    args = parser.parse_args(argv)
    if not args.command:
        print(PURPOSE)
        print("Try: hanani factors | hanani workflow status")
        return 0

    if args.command == "workflow" and not getattr(args, "workflow_command", None):
        print(workflow_status())
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())