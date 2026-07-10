# Hanani — Geopolitical News Reasoning

**Hanani** is a standalone geopolitical **reasoning system** — expandable semantic
graphs + a layered assessment engine, not a one-off crisis briefing or news reader.

> What do all available reports imply when combined?

**Requirements (web):** run `hanani docs serve` → http://127.0.0.1:8765/

Architecture: [`docs/reasoning-system.md`](docs/reasoning-system.md) ·
[`docs/requirements.md`](docs/requirements.md)

Initial focus: Russia–Ukraine, Hormuz Strait / US–Iran–Gulf states.

See [`docs/vision.md`](docs/vision.md).

```bash
hanani --help
hanani factors
hanani reasoning         # engine status (Layer 1 → Layer 2 pipeline)
hanani ontology          # mechanism graph (L1–L5)
hanani rhetoric          # fallacy / audit graph
hanani workflow status
hanani docs serve          # requirements + architecture as web pages
```

Graphs: [`living-semantic-model.md`](docs/ontology/living-semantic-model.md) ·
[`rhetorical-logic-graph.md`](docs/ontology/rhetorical-logic-graph.md)

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