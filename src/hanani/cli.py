"""CLI for Hanani — Geopolitical News Reasoning."""

from __future__ import annotations

import argparse
import sys

from hanani import __version__
from hanani.factors import list_factors

PURPOSE = (
    "Hanani — Geopolitical News Reasoning.\n"
    "News synthesis instance of Valhalla. Asks: 'What do all available reports\n"
    "imply when combined?' Orchestration: valhalla (separate package/repo).\n"
)


def _cmd_factors(_: argparse.Namespace) -> int:
    for factor in list_factors():
        print(f"  {factor['id']:30s}  {factor['label']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hanani", description=PURPOSE)
    parser.add_argument("--version", action="version", version=f"hanani {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("factors", help="List factor taxonomy").set_defaults(func=_cmd_factors)

    args = parser.parse_args(argv)
    if not args.command:
        print(PURPOSE)
        print("Try: hanani factors  |  valhalla status  |  valhalla instances")
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())