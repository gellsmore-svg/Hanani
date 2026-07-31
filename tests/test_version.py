"""`hanani.__version__` must not drift from the packaged version.

It was hand-maintained and sat at 0.1.0 while the distribution shipped 0.8.0.
That is not cosmetic: it is what `hanani --version` prints and what the Keturah
manifest advertises to the family registry and MCP consumers, so a stale
literal misreports Hanani's capabilities everywhere they are federated.
"""

from __future__ import annotations

import re
import tomllib
from importlib.metadata import version as pkg_version
from pathlib import Path

import hanani
from hanani.manifest import build_manifest


def test_version_matches_the_installed_distribution():
    assert hanani.__version__ == pkg_version("hanani")


def test_version_matches_pyproject():
    """Guards the other direction: bumping pyproject must be all it takes."""
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    declared = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
    assert hanani.__version__ == declared


def test_manifest_advertises_the_real_version():
    assert build_manifest().version == pkg_version("hanani")


def test_version_is_not_a_hardcoded_literal():
    """The regression itself: no version string restated in __init__.py."""
    source = Path(hanani.__file__).read_text(encoding="utf-8")
    assert not re.search(r'^__version__\s*=\s*["\']\d+\.\d+', source, re.M), (
        "__version__ is hardcoded again — derive it from importlib.metadata so "
        "it cannot drift from pyproject."
    )
