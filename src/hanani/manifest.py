"""Keturah capability manifest for Hanani."""

from __future__ import annotations

from hanani import __version__


def capabilities() -> dict:
    try:
        from keturah import capability, manifest
    except ImportError:
        return {
            "product": "hanani",
            "version": __version__,
            "capabilities": [],
            "note": "Install keturah for full manifest schema.",
        }

    caps = [
        capability(
            "factors",
            "List the geopolitical factor taxonomy.",
            input_schema={"type": "object", "properties": {}},
        ),
    ]
    return manifest("hanani", version=__version__, capabilities=caps).to_dict()