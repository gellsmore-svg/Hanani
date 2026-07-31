"""Hanani — the Intelligence Synthesis Engine.

Multi-source geopolitical evidence synthesis with inspectable reasoning.
See docs/philosophy.md.
"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    # Single source of truth: read the installed distribution's version rather
    # than restating it here. A hand-maintained literal silently drifts from
    # pyproject — this one sat at 0.1.0 while the package shipped 0.8.0, and it
    # is what `hanani --version` prints and what the Keturah manifest (and so
    # MCP consumers) advertise.
    __version__ = _pkg_version("hanani")
except PackageNotFoundError:  # running straight from a source checkout
    __version__ = "0.0.0+source"

__all__ = ["__version__"]
