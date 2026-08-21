"""Serve Hanani documentation site."""

from __future__ import annotations

import argparse
import http.server
import subprocess
import sys
from pathlib import Path

def _checkout_root() -> Path | None:
    """Repo root when running from a git checkout; None in a wheel/pipx install."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "docs" / "web").is_dir() and (parent / "pyproject.toml").is_file():
            return parent
    return None


ROOT = _checkout_root() or Path(__file__).resolve().parents[2]
WEB = ROOT / "docs" / "web"
BUILD = ROOT / "scripts" / "build_docs.py"


def build_docs() -> int:
    if not BUILD.is_file():
        print(
            "hanani docs serve is a checkout tool (docs/ are not in the wheel). "
            "Clone https://github.com/gellsmore-svg/Hanani and run from the repo.",
            file=sys.stderr,
        )
        return 2
    return subprocess.call([sys.executable, str(BUILD)], cwd=ROOT)


def serve(port: int = 8805, *, rebuild: bool = True) -> int:
    if rebuild:
        code = build_docs()
        if code != 0:
            return code
    if not WEB.exists():
        print(f"missing docs site: {WEB}", file=sys.stderr)
        return 1

    handler = http.server.SimpleHTTPRequestHandler

    class _Handler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(WEB), **kwargs)

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Serving Hanani docs at {url}")
    print("  Requirements: /  ·  Ontology: /ontology.html  ·  Architecture: /architecture.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and serve Hanani documentation.")
    parser.add_argument("command", nargs="?", choices=["build", "serve"], default="serve")
    parser.add_argument("-p", "--port", type=int, default=8805)
    parser.add_argument("--no-rebuild", action="store_true", help="Serve without rebuilding")
    args = parser.parse_args(argv)
    if args.command == "build":
        return build_docs()
    return serve(args.port, rebuild=not args.no_rebuild)


if __name__ == "__main__":
    raise SystemExit(main())