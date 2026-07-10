from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_build_docs_produces_index() -> None:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "build_docs.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    index = root / "docs" / "web" / "index.html"
    assert index.exists()
    text = index.read_text(encoding="utf-8")
    assert "REQ-HANANI-001" in text
    assert "FR-REASON-01" in text