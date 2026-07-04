# Hanani — Geopolitical News Reasoning

**Hanani** is a standalone geopolitical news *reasoning* platform — an evidence
synthesis engine, not a news reader.

> What do all available reports imply when combined?

Initial focus: Russia–Ukraine, Hormuz Strait / US–Iran–Gulf states.

See [`docs/vision.md`](docs/vision.md).

```bash
hanani --help
hanani factors
hanani workflow status
```

## Family stack

| Sibling | Role |
|---|---|
| Milcah | argument evaluation, multi-LLM debate |
| Tirzah | memory over ingested reports |
| Hoglah | LLM execution queue |
| Galeed | process trace |
| Keturah | capability manifest |

## Develop

```bash
pip install -e "../Keturah"
pip install -e ".[dev]"
pytest
```

## License

[Apache License 2.0](LICENSE).