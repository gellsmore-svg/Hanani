# Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         Hanani                                   │
│  ┌─────────────────────┐    ┌─────────────────────┐              │
│  │ Mechanism graph (A) │    │ Rhetoric graph (B)  │              │
│  │ L1–L5 + factors     │    │ fallacies + audit   │              │
│  └──────────┬──────────┘    └──────────┬──────────┘              │
│             └────────────┬─────────────┘                         │
│                          ▼                                       │
│              reasoning engine (Layer 1 → Layer 2)                │
│                          ▼                                       │
│         logic atoms · assessment records · analysis graph        │
│                          ▼                                       │
│              [Phase 3] narrative + outcome scenarios             │
│                          ▼                                       │
│                   workflow (orchestration)                       │
└────────────────────────────┬─────────────────────────────────────┘
                             ▼
        ┌───────────────────────────────────────────┐
        │  Milcah  Tirzah  Hoglah  Galeed           │
        └───────────────────────────────────────────┘
```

| Package | Role |
|---|---|
| `hanani.ontology` | Mechanism graph seed |
| `hanani.rhetoric` | Rhetoric graph seed |
| `hanani.graph` | Unified node/edge store |
| `hanani.reasoning` | Layered atom assessment pipeline |
| `hanani.factors` | Observable variables linked from mechanisms |
| `hanani.workflow` | Batch orchestration, Milcah scheduling |

Detail: [`reasoning-system.md`](reasoning-system.md).