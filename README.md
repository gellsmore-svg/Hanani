# Hanani — Geopolitical News Reasoning

**Hanani** is the **geopolitical news instance** of
[Valhalla](https://github.com/gellsmore-svg/Valhalla) — an evidence synthesis
and reasoning engine, not a news reader.

It asks not *"What happened?"* but *"What do all available reports imply when
combined?"* — applying every extractable factor from multiple reports across
the theatres you follow (Russia–Ukraine, Hormuz Strait / US–Iran–Gulf states).

See [`docs/vision.md`](docs/vision.md) for the full design intent.

```bash
hanani --help
hanani factors             # factor taxonomy
```

Orchestration: `valhalla status` | `valhalla instances`

## Core capabilities

- Multi-source ingestion and claim extraction
- Evidence graph (corroboration / conflict edges)
- Factor identification as explicit variables
- Competing hypotheses with multi-LLM debate (via Milcah through Valhalla)
- Structural confidence estimates — not popularity-based
- Inspectable reasoning traces

## Family

| Component | Role |
|---|---|
| [Valhalla](https://github.com/gellsmore-svg/Valhalla) | reasoning orchestration platform |
| Milcah | argument evaluation, multi-LLM debate |
| Tirzah | memory over ingested reports |
| Hoglah | LLM execution queue |
| Galeed | process trace |
| [Ed](https://github.com/gellsmore-svg/Ed) | scripture translation instance (separate) |

## Develop

```bash
pip install -e "../Keturah" -e "../Valhalla"
pip install -e ".[dev]"
pytest
```

## License

[Apache License 2.0](LICENSE).