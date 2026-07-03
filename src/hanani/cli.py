"""CLI for Hanani — the Intelligence Synthesis Engine."""

from __future__ import annotations

import argparse
import sys

from hanani import __version__
from hanani.factors import list_factors
from hanani.valhalla import valhalla_status

PURPOSE = (
    "Hanani — the Intelligence Synthesis Engine.\n"
    "Multi-source geopolitical evidence synthesis with inspectable reasoning.\n"
    "Guiding question:\n"
    "  'What do all available reports imply when combined?'\n"
)


def _cmd_factors(_: argparse.Namespace) -> int:
    for factor in list_factors():
        print(f"  {factor['id']:30s}  {factor['label']}")
    return 0


def _cmd_valhalla_status(_: argparse.Namespace) -> int:
    print(valhalla_status())
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hanani", description=PURPOSE)
    parser.add_argument("--version", action="version", version=f"hanani {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("factors", help="List factor taxonomy").set_defaults(func=_cmd_factors)

    valhalla = sub.add_parser("valhalla", help="Valhalla orchestration layer")
    valhalla_sub = valhalla.add_subparsers(dest="valhalla_command")
    valhalla_sub.add_parser("status", help="Orchestration status").set_defaults(
        func=_cmd_valhalla_status
    )

    args = parser.parse_args(argv)
    if not args.command:
        print(PURPOSE)
        print("Try: hanani factors | hanani valhalla status")
        return 0

    if args.command == "valhalla" and not getattr(args, "valhalla_command", None):
        print(valhalla_status())
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())