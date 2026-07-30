# Hanani — Geopolitical News Reasoning

**Hanani** is a standalone geopolitical **reasoning system** — expandable semantic
graphs + a layered assessment engine, not a one-off crisis briefing or news reader.

> What do all available reports imply when combined?

**Requirements (web):** run `hanani docs serve` → http://127.0.0.1:8805/

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

# The vertical slice — article → atoms → Layer 1 rhetoric → Layer 2 → persisted:
hanani ingest article.txt --source-id reuters --title "Odesa depot strike"
hanani ingest article.txt --source-id reuters --hoglah-model llama3   # + model tier
hanani corpus              # summarise the persisted store (~/.hanani)
hanani gaps                # registry-aware gaps and stated information needs
hanani relations           # typed, auditable relations between assessed atoms
hanani push-tirzah         # push stored records into Tirzah memory (tirzah extra)
hanani debate              # Milcah multi-LLM debate over admissible atoms (milcah extra)
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
