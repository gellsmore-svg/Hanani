# Hanani

**Hanani asks of the news: what do all available reports imply when
combined?** It breaks each article into *logic atoms* (individual claims),
checks how each claim is argued, tags it against the mechanisms that drive
geopolitics, and keeps the results in a store that grows as you ingest more
sources. Initial theatres are Russia–Ukraine and the Strait of Hormuz
(US–Iran–Gulf states).

It is a reusable reasoning engine, not a news reader or a one-off briefing.
Sources are judged by how they argue, never by outlet reputation.

## Is it for you?

**Good fit:** you analyse a conflict or region across many reports and want
every claim checked the same auditable way, with the reasoning stored rather
than summarised away.

**Not a fit (yet):** you want a finished assessment or forecast. The synthesis
and narrative stages are designed but not built (see [Status](#status)).

## Try it

```bash
pipx install hanani
hanani ingest article.txt --source-id reuters --title "Odesa depot strike"
```

```
article: reuters-b8e1694704e8  (reuters: Odesa depot strike)
  atoms: 4  admissible→Layer2: 2
  robustness: {'Weak': 2, 'Strong': 2}
  rhetoric floor: 7/32 vocabulary keys detectable offline — Weak only when a floor cue or model hit fires; Strong is not a full audit
  model tier: off (deterministic floor)
```

Then explore what has accumulated:

```bash
hanani corpus        # what the store (~/.hanani, or --store DIR) holds
hanani gaps          # what is missing, and stated information needs
hanani relations     # typed, auditable links between assessed atoms
```

No model is needed. Add `--hoglah-model llama3` to `ingest` for a model tier
on top of the deterministic floor (needs `hanani[hoglah]`).

## How it works

1. **Atoms.** An article is split into logic atoms, each traceable to its
   source text.
2. **Layer 1, rhetoric.** Each atom is checked against a rhetorical graph of
   fallacies, warrant gaps and closure-versus-inquiry patterns and rated
   *Weak* or *Strong*. Only admissible atoms continue.
3. **Layer 2, mechanisms.** Admissible atoms are tagged against a five-layer
   mechanism graph (security dilemma, prospect theory, costly signalling,
   spirals and others) and observable factors (logistics, sanctions,
   production and so on).
4. **Store.** Atoms, ratings and relations persist as JSONL, so each new
   source is assessed against everything already ingested.

The two graphs are described in
[living-semantic-model.md](docs/ontology/living-semantic-model.md) and
[rhetorical-logic-graph.md](docs/ontology/rhetorical-logic-graph.md); the full
architecture is in [reasoning-system.md](docs/reasoning-system.md).

## Status

`hanani reasoning` reports this live:

- **Offline, only 7 of 27 fallacy patterns are detectable.** "Strong" means
  that no detectable problem fired, not that the atom passed a full audit. A
  model tier widens coverage.
- **Audit criteria are a scaffold.** Six are declared; their scores are stored
  as *unassessed* until they are implemented.
- **Summary and narrative synthesis are not built yet.** The pipeline ends at
  Layer 2.

## With the rest of the family

All optional, as extras (`pipx inject hanani 'hanani[family]'` for all of them):

| Sibling | Command | Purpose |
|---|---|---|
| [Hoglah](https://github.com/gellsmore-svg/hoglah) | `ingest --hoglah-model …` | Queued model calls for the model tier |
| [Milcah](https://github.com/gellsmore-svg/Milcah) | `hanani debate` | Multi-LLM debate over admissible atoms |
| [Tirzah](https://github.com/gellsmore-svg/tirzah) | `hanani push-tirzah` | Push stored records into Tirzah memory |
| [Galeed](https://github.com/gellsmore-svg/galeed) | — | Declared as an extra, but nothing emits traces yet |
| [Keturah](https://github.com/gellsmore-svg/keturah) | — | Capability manifest (a required dependency) |

## More

- `hanani --help` for every command, including `factors`, `ontology`,
  `rhetoric` and `workflow status`.
- `hanani docs serve` serves the requirements and architecture at
  http://127.0.0.1:8805/ (from a git checkout; the docs are not in the wheel).
- [Vision](docs/vision.md) · [requirements](docs/requirements.md) ·
  [philosophy](docs/philosophy.md) · [2026-08-08 review](docs/review-2026-08-08.md)
- Develop: `pip install -e ".[dev]" && pytest`

[CHANGELOG](CHANGELOG.md) · [CONTRIBUTING](CONTRIBUTING.md) ·
[SECURITY](SECURITY.md) · Apache 2.0, see [LICENSE](LICENSE).
