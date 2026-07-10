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
    assert "Geopolitical News Reasoning" in result.stdout


def test_workflow_status_scaffold():
    from hanani.workflow import workflow_status

    assert "scaffold" in workflow_status()


def test_factors_non_empty():
    from hanani.factors import list_factors

    assert len(list_factors()) >= 10


def test_ontology_cli_lists_layers():
    from hanani.ontology import ONTOLOGY_VERSION, list_layers

    assert ONTOLOGY_VERSION == "0.1"
    assert len(list_layers()) == 5


def test_factors_include_propaganda():
    from hanani.factors import list_factors

    ids = {f["id"] for f in list_factors()}
    assert "propaganda-signals" in ids