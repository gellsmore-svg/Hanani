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


def test_installed_console_script_factors_and_workflow_status():
    """#2: exercise the installed ``hanani`` entry point, not only ``-m``."""
    import shutil
    from pathlib import Path

    # Prefer the venv console script when running under pytest in a venv.
    script = shutil.which("hanani")
    if script is None:
        # Editable install places scripts next to the test interpreter.
        candidate = Path(sys.executable).resolve().parent / "hanani"
        script = str(candidate) if candidate.is_file() else None
    if not script:
        import pytest

        pytest.skip("hanani console script not on PATH (pip install -e .)")

    factors = subprocess.run(
        [script, "factors"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert factors.returncode == 0, factors.stderr
    assert factors.stdout.strip()

    status = subprocess.run(
        [script, "workflow", "status"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert status.returncode == 0, status.stderr
    assert "vertical-slice" in status.stdout or "ingest" in status.stdout


def test_workflow_status_vertical_slice():
    from hanani.workflow import workflow_status

    assert "vertical-slice" in workflow_status()
    assert "ingest" in workflow_status()


def test_factors_non_empty():
    from hanani.factors import list_factors

    assert len(list_factors()) >= 10


def test_ontology_cli_lists_layers():
    from hanani.ontology import ONTOLOGY_VERSION, list_layers

    assert ONTOLOGY_VERSION == "0.3"
    assert len(list_layers()) == 5


def test_factors_include_propaganda():
    from hanani.factors import list_factors

    ids = {f["id"] for f in list_factors()}
    assert "propaganda-signals" in ids


def test_rhetoric_cli_reports_declared_vs_offline(capsys):
    from hanani.cli import main

    assert main(["rhetoric"]) == 0
    out = capsys.readouterr().out
    assert "declared" in out and "detectable offline" in out


def test_asssib_cli_distinguishes_schema_from_operational(capsys):
    from hanani.cli import main

    assert main(["asssib"]) == 0
    out = capsys.readouterr().out
    assert "schema ready" in out.lower()
    assert "operationally wired" in out.lower()


def test_debate_missing_extra_exits_nonzero(tmp_path, monkeypatch):
    """Review F4/M3: optional-extra failure must not look like success."""
    import hanani.debate as dbt
    from hanani.cli import main
    from hanani.pipeline import ingest_and_assess
    from hanani.store import SliceStore

    store = SliceStore(tmp_path)
    ingest_and_assess(
        "Grain volumes fell fifteen percent in June after port strikes resumed.",
        source_id="wire", title="t", store=store,
    )

    def boom(_extractor):
        raise ImportError("No module named 'milcah'")

    monkeypatch.setattr(dbt, "_milcah_run", boom)
    rc = main(["debate", "--store", str(tmp_path)])
    assert rc != 0