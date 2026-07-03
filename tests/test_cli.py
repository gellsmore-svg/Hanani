"""Smoke tests for Hanani v0.1 scaffold."""

from __future__ import annotations

import subprocess
import sys


def test_cli_no_args_prints_purpose():
    result = subprocess.run(
        [sys.executable, "-m", "hanani.cli"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Intelligence Synthesis Engine" in result.stdout


def test_factors_non_empty():
    from hanani.factors import list_factors

    assert len(list_factors()) >= 10


def test_valhalla_status_scaffold():
    from hanani.valhalla import valhalla_status

    assert "scaffold" in valhalla_status()