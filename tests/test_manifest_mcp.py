"""Federation surfaces: build_manifest + MCP handlers align by name."""

from __future__ import annotations

import pytest

keturah = pytest.importorskip("keturah")

from hanani.manifest import build_manifest, capabilities  # noqa: E402
from hanani.mcp_handlers import build_handlers  # noqa: E402
from hanani.store import SliceStore  # noqa: E402

_ARTICLE = (
    "Insurance premiums for Black Sea grain shipments have risen by roughly a "
    "third since strikes on port infrastructure resumed last month. "
    "The West now has only two options: escalate or watch the corridor close."
)


def test_build_manifest_declares_slice_capabilities() -> None:
    m = build_manifest()
    names = [c.name for c in m.capabilities]
    assert names == ["ingest_and_assess", "corpus_summary", "factors"]
    ingest = m.capabilities[0]
    assert set(ingest.input_schema["required"]) == {"text", "source_id", "title"}


def test_capabilities_dict_back_compat() -> None:
    data = capabilities()
    assert data["product"] == "hanani"
    assert any(c["name"] == "ingest_and_assess" for c in data["capabilities"])


def test_every_manifest_tool_has_a_handler() -> None:
    """The MCP server only lists handler-backed tools — keep the two aligned."""
    declared = {f"hanani.{c.name}" for c in build_manifest().capabilities}
    handlers = set(build_handlers(store=SliceStore("/tmp/unused")))
    missing = declared - handlers
    assert not missing, f"manifest tools without handlers: {sorted(missing)}"


def test_ingest_handler_end_to_end(tmp_path) -> None:
    handlers = build_handlers(store=SliceStore(tmp_path))
    out = handlers["hanani.ingest_and_assess"](
        text=_ARTICLE, source_id="reuters", title="Grain corridor"
    )
    assert out["atom_count"] >= 1 and "error" not in out

    summary = handlers["hanani.corpus_summary"]()
    assert summary["article_count"] == 1

    assert "error" in handlers["hanani.ingest_and_assess"](text="", source_id="s", title="t")
    assert "error" in handlers["hanani.ingest_and_assess"](text="x" * 50, source_id="", title="")


def test_factors_handler() -> None:
    out = build_handlers(store=SliceStore("/tmp/unused"))["hanani.factors"]()
    assert out["factors"] and all("id" in f for f in out["factors"])
