"""Vertical slice: ingest one article → atoms → Layer 1 → Layer 2 → persist.

The first *executable* path through Hanani's reasoning design (everything before
this was schema + vocabulary). Family pattern throughout: a **deterministic
floor** that always runs offline, plus an optional **model tier** via an
injectable ``ask: Callable[[str], str]`` (wire Hoglah with :func:`hoglah_ask`).
The model tier is best-effort — bad output falls back to the floor, and model
fallacy claims are validated against the rhetoric vocabulary, never trusted raw.
"""

from __future__ import annotations

import json
import re
import time
from typing import Any, Callable

from hanani.reasoning import LogicAtom, ReasoningEngine, default_engine
from hanani.rhetoric import ENTHYMEME_PATTERNS, FALLACIES
from hanani.sources import SourceCorpus, content_hash, default_corpus
from hanani.store import SliceStore

AskFn = Callable[[str], str]

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_MIN_ATOM_CHARS = 40

# Conservative deterministic cues → rhetoric-graph hits. Deliberately few and
# high-precision: this is the offline floor, not the audit of record.
# Expanded 2026-08-08 (review H1) for common analytic fallacies that were
# scoring Strong and propagating with no model tier available.
_CUE_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("fallacy.false_dilemma",
     re.compile(r"\bonly (?:two|one)\b|\bno (?:other )?(?:choice|alternative)\b|\beither\b.{3,80}\bor\b", re.I | re.S)),
    ("fallacy.slippery_slope",
     re.compile(r"\binevitabl\w*\b|\bspiral(?:ing)? into\b|\bslide toward\b|\bdomino\b", re.I)),
    ("fallacy.appeal_to_authority_in_text",
     re.compile(
         r"\bexperts (?:say|agree|warn)\b"
         r"|\bofficials? said?\b"
         r"|\banalysts agree\b"
         r"|\bbecause (?:the )?\w[\w\s-]{0,40}\b(?:said|says|stated|claims)\b"
         r"|\bthis is true because\b",
         re.I,
     )),
    ("fallacy.rhetoric_action_conflation",
     re.compile(r"\bvow(?:s|ed)? to\b|\bthreat(?:en(?:s|ed)?)? to\b.*\bproves\b", re.I)),
    ("fallacy.appeal_to_common_belief",
     re.compile(
         r"\beveryone knows\b"
         r"|\bit is widely (?:accepted|known|believed)\b"
         r"|\bas (?:everybody|everyone) knows\b"
         r"|\bno one (?:seriously )?disputes\b"
         r"|\bit is common knowledge\b",
         re.I,
     )),
    ("fallacy.ad_hominem_in_text",
     re.compile(
         r"\banyone who (?:doubts|disagrees|questions)\b"
         r"|\bthose who (?:doubt|disagree|question)\b"
         r"|\bare (?:simply |just )?(?:apologists|stooges|puppets|naive)\b"
         r"|\bhas not been paying attention\b"
         r"|\bonly a (?:fool|idiot|traitor)\b"
         r"|\bKremlin apologists\b",
         re.I,
     )),
    ("fallacy.circular_reasoning",
     re.compile(
         r"\bproves the theory\b.{0,80}\btheory explains\b"
         r"|\bthe theory\b.{0,40}\bexplains the\b.{0,40}\bproves\b"
         r"|\bas proven by the fact that it is proven\b",
         re.I | re.S,
     )),
)


def offline_cue_keys() -> frozenset[str]:
    """Rhetoric-graph keys reachable by the deterministic floor alone."""
    return frozenset(key for key, _ in _CUE_RULES)


def rhetoric_floor_coverage() -> dict[str, int | float | list[str]]:
    """Declared vocabulary size vs offline-detectable keys (review F2/M4)."""
    declared = sorted(set(FALLACIES) | {k for k in ENTHYMEME_PATTERNS})
    offline = sorted(offline_cue_keys())
    total = len(declared)
    detectable = len(offline)
    return {
        "declared": total,
        "detectable_offline": detectable,
        "offline_keys": offline,
        "coverage_rate": (detectable / total) if total else 0.0,
    }


# --- atom extraction --------------------------------------------------------


def extract_atoms(
    text: str, *, source_id: str, ask: AskFn | None = None, max_atoms: int = 10
) -> list[LogicAtom]:
    """Split an article into candidate logic atoms (claim-bearing sentences).

    Deterministic floor: sentence segmentation, keeping substantive sentences.
    Model tier (``ask``): the model proposes claim strings (JSON array); output
    is validated and capped, and any failure falls back to the floor.
    """
    claims: list[str] = []
    if ask is not None:
        claims = _ask_claims(ask, text, max_atoms)
    if not claims:
        sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text or "")]
        claims = [s for s in sentences if len(s) >= _MIN_ATOM_CHARS][:max_atoms]
    return [
        LogicAtom(
            atom_id=f"atom-{content_hash(claim)[:10]}",
            source_id=source_id,
            text=claim,
        )
        for claim in claims
    ]


def _ask_claims(ask: AskFn, text: str, max_atoms: int) -> list[str]:
    prompt = (
        "Extract the distinct factual or causal CLAIMS asserted in this news "
        "text. Return ONLY a JSON array of claim strings (verbatim or lightly "
        f"normalised), at most {max_atoms}.\n\nTEXT:\n{text[:6000]}"
    )
    try:
        raw = ask(prompt)
        data = json.loads(raw[raw.index("[") : raw.rindex("]") + 1])
        return [c.strip() for c in data if isinstance(c, str) and len(c.strip()) >= 10][:max_atoms]
    except Exception:  # noqa: BLE001 - model tier is best-effort
        return []


# --- Layer 1 rhetoric hits ---------------------------------------------------


def detect_rhetoric_hits(text: str, *, ask: AskFn | None = None) -> list[str]:
    """Rhetoric-graph hits for one atom: deterministic cues + optional model audit.

    Model output is validated against the FALLACIES / ENTHYMEME_PATTERNS
    vocabulary — an unknown key from the model is dropped, never invented.
    """
    hits = {key for key, pattern in _CUE_RULES if pattern.search(text or "")}
    if ask is not None:
        hits.update(_ask_hits(ask, text))
    return sorted(hits)


def _ask_hits(ask: AskFn, text: str) -> set[str]:
    vocabulary = sorted(FALLACIES) + sorted(ENTHYMEME_PATTERNS)
    prompt = (
        "Audit this single claim against the fallacy/enthymeme vocabulary. "
        "Return ONLY a JSON array of matching keys from the vocabulary "
        "(empty array if clean).\n\nVOCABULARY:\n"
        + "\n".join(vocabulary)
        + f"\n\nCLAIM:\n{text[:2000]}"
    )
    try:
        raw = ask(prompt)
        data = json.loads(raw[raw.index("[") : raw.rindex("]") + 1])
        allowed = set(vocabulary)
        return {k for k in data if isinstance(k, str) and k in allowed}
    except Exception:  # noqa: BLE001 - model tier is best-effort
        return set()


# --- the slice ---------------------------------------------------------------


def ingest_and_assess(
    text: str,
    *,
    source_id: str,
    title: str,
    provenance: str = "manual",
    ask: AskFn | None = None,
    store: SliceStore | None = None,
    corpus: SourceCorpus | None = None,
    engine: ReasoningEngine | None = None,
    max_atoms: int = 10,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the full slice on one article and persist the results.

    Returns a summary: article id, atom count, per-tier robustness, and how many
    atoms passed the Layer-1 admissibility gate into Layer 2.
    """
    if not (text or "").strip():
        raise ValueError("article text is required")
    corpus = corpus or default_corpus()
    engine = engine or default_engine()
    store = store or SliceStore()

    article = corpus.register(
        source_id=source_id, title=title, text=text,
        provenance=provenance, metadata=metadata,
    )
    atoms = extract_atoms(text, source_id=source_id, ask=ask, max_atoms=max_atoms)
    records = []
    robustness: dict[str, int] = {}
    admissible = 0
    for atom in atoms:
        hits = detect_rhetoric_hits(atom.text, ask=ask)
        record = engine.assess_atom(atom, rhetoric_hits=hits)
        tier = record.layer1.robustness if record.layer1 else "unknown"
        robustness[tier] = robustness.get(tier, 0) + 1
        if record.layer2 is not None:
            admissible += 1
        records.append(record)
    corpus.link_atoms(article.article_id, [a.atom_id for a in atoms])

    # FR-ASSSIB-06: assessed atoms emit explicit speed-differential edges into
    # the analysis graph (empty until an assessment carries speed evidence).
    from dataclasses import asdict

    from hanani.assib import speed_edges_from_assessment

    edges = [asdict(e) for r in records for e in speed_edges_from_assessment(r)]

    store.save_article(article.to_dict())
    store.save_assessments(article.article_id, [r.to_dict() for r in records])
    store.save_graph_edges(article.article_id, edges)

    return {
        "article_id": article.article_id,
        "source_id": source_id,
        "title": title,
        "atom_count": len(atoms),
        "admissible_atoms": admissible,
        "robustness": robustness,
        "speed_edges": len(edges),
        "model_tier": ask is not None,
        "store_dir": str(store.directory),
    }


# --- optional Hoglah model tier ----------------------------------------------


def hoglah_ask(
    model: str, *, timeout: float = 180.0, poll_interval: float = 2.0
) -> AskFn | None:
    """An ``ask`` backed by the Hoglah queue (family Hoglah-first LLM policy).

    Returns None when the hoglah library isn't installed — callers then run the
    deterministic floor only. Requires a running Hoglah worker to complete jobs.
    """
    try:
        from hoglah import Hoglah, JobStatus
    except Exception:  # noqa: BLE001 - optional extra
        return None

    client = Hoglah(start_worker=False)
    terminal_bad = {JobStatus.FAILED, JobStatus.CANCELLED} if hasattr(JobStatus, "FAILED") else set()

    def ask(prompt: str) -> str:
        job_id = client.submit(prompt=prompt, model=model, step_name="hanani.slice")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = client.get(job_id)
            status = getattr(result, "status", None)
            if getattr(result, "output", None):
                return str(result.output)
            if status in terminal_bad:
                raise RuntimeError(f"hoglah job {job_id} ended {status}")
            time.sleep(poll_interval)
        raise TimeoutError(f"hoglah job {job_id} did not finish in {timeout}s")

    return ask
