# Architecture — Intelligence Synthesis Engine v0.1

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                      Hanani                             │
│  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │  factors / claims    │  │  evidence graph         │  │
│  └──────────┬───────────┘  └────────────┬────────────┘  │
│             └──────────────┬─────────────┘              │
│                            ▼                            │
│                     ┌─────────────┐                     │
│                     │  Valhalla   │                     │
│                     └──────┬──────┘                     │
└────────────────────────────┼────────────────────────────┘
                             ▼
        ┌───────────────────────────────────────────┐
        │  Milcah  Tirzah  Hoglah  Galeed  Mahalath │
        └───────────────────────────────────────────┘
```

## Pipeline (target)

```
News feeds / documents
  → semantic + claim extraction
  → evidence graph construction
  → factor identification
  → competing hypotheses
  → multi-LLM debate (corroboration / conflict / propaganda)
  → confidence estimates + scenario notes
  → trace
```

## Trace shape (draft)

- `synthesis_id`, `theatre`, `factor_profile`
- `reports[]` — source, excerpt, weight, bias class
- `factors[]` — id, value, confidence
- `hypotheses[]` — statement, support, opposition
- `debate_rounds[]` — model, argument, citations
- `outcome` — conclusion + uncertainty state

See [`architecture-decisions.md`](architecture-decisions.md).