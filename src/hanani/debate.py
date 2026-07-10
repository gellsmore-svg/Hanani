"""Multi-LLM debate over assessed atoms — the Milcah increment.

Hanani does not grow its own debate engine: the admissible atoms (those that
survived the Layer-1 rhetoric gate) are composed into the guiding question —
*what do all available reports imply when combined?* — and pressure-tested by
**Milcah**, the family's multi-LLM coherence/debate specialist, through its
public contract (``run_specialist``: never leaks exceptions, returns a bounded,
evidenced verdict).

Inadmissible atoms are deliberately excluded and reported: rhetoric that failed
the gate must not smuggle itself into the debate as evidence. The Milcah runner
is injectable for tests; ``extractor="hoglah"`` selects Milcah's LLM quality
path, the default is its deterministic rule pipeline.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from hanani.store import SliceStore

RunFn = Callable[[dict[str, Any]], Any]

GUIDING_QUESTION = (
    "What do all available reports imply when combined? Pressure-test the "
    "coherence of the combined claim set below: identify contradictions, "
    "unsupported leaps, and what would have to be true for the combined "
    "picture to hold."
)


def build_debate_input(
    assessments: list[dict[str, Any]],
) -> tuple[str, str, list[str], list[str]]:
    """Compose (query, context, debated_atom_ids, excluded_atom_ids).

    Only Layer-2-admissible atoms enter the debate context; gated atoms are
    excluded and listed so the exclusion is auditable.
    """
    admissible: list[dict[str, Any]] = []
    excluded: list[str] = []
    for record in assessments:
        atom = record.get("atom") or {}
        if record.get("layer2") is None:
            excluded.append(str(atom.get("atom_id", "?")))
        else:
            admissible.append(record)

    lines = []
    for index, record in enumerate(admissible, start=1):
        atom = record.get("atom") or {}
        layer1 = record.get("layer1") or {}
        lines.append(
            f"{index}. [{atom.get('source_id', '?')} | "
            f"{layer1.get('robustness', '?')}] {str(atom.get('text', '')).strip()}"
        )
    context = "COMBINED CLAIM SET (Layer-1 admissible atoms):\n" + "\n".join(lines)
    debated = [str((r.get("atom") or {}).get("atom_id", "?")) for r in admissible]
    return GUIDING_QUESTION, context, debated, excluded


def _verdict_dict(result: Any) -> dict[str, Any]:
    """Normalise a SpecialistResult (object or mapping) to the contract dict."""
    get = result.get if isinstance(result, dict) else lambda k, d=None: getattr(result, k, d)
    return {
        "claims": list(get("claims", []) or []),
        "objections": list(get("objections", []) or []),
        "evidence": list(get("evidence", []) or []),
        "citations": list(get("citations", []) or []),
        "confidence": float(get("confidence", 0.0) or 0.0),
        "terminal_reason": str(get("terminal_reason", "") or ""),
    }


def _milcah_run(extractor: str = "rule") -> RunFn:
    """The real Milcah specialist chain (requires the ``milcah`` extra)."""
    from milcah.specialist import SpecialistConfig, run_specialist

    config = SpecialistConfig(extractor=extractor)

    def run(request: dict[str, Any]) -> Any:
        return run_specialist(request, config=config)

    return run


def debate_corpus(
    store: SliceStore,
    *,
    article_id: str | None = None,
    max_iterations: int = 3,
    extractor: str = "rule",
    session_id: str = "hanani",
    run: RunFn | None = None,
) -> dict[str, Any]:
    """Debate the admissible atoms (one article, or the whole store) via Milcah.

    Persists and returns the debate record: scope, debated/excluded atom ids,
    and the bounded Milcah verdict (claims/objections/evidence/confidence/
    terminal_reason).
    """
    if run is None:
        try:
            run = _milcah_run(extractor)
        except Exception as error:  # noqa: BLE001 - the extra may be missing
            raise RuntimeError(
                "debate needs the milcah extra (pip install 'hanani[milcah]'): "
                f"{error}"
            ) from error

    assessments = store.assessments(article_id)
    if article_id is not None and not assessments:
        raise ValueError(f"unknown article_id in store: {article_id}")
    query, context, debated, excluded = build_debate_input(assessments)
    if not debated:
        raise ValueError("no admissible atoms to debate (all failed the Layer-1 gate)")

    result = run(
        {
            "query": query,
            "mode": "coherence",
            "context": context,
            "max_iterations": max(1, int(max_iterations)),
            "session_id": session_id,
        }
    )
    record = {
        "debated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": article_id or "corpus",
        "article_id": article_id,
        "debated_atom_ids": debated,
        "excluded_inadmissible": excluded,
        "extractor": extractor,
        "verdict": _verdict_dict(result),
    }
    store.save_debate(record)
    return record
