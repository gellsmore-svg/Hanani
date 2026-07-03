# Vision — Geopolitical News Reasoning System

Hanani is a **specialised instance** of
[Valhalla](https://github.com/gellsmore-svg/Valhalla) — not the platform itself.

## What this is

Not a news reader. An **evidence synthesis and reasoning engine** that asks:

> What do all available reports imply when combined?

—not merely *What happened?*

## Initial theatres

The user follows multiple channels on:

- the **Russia–Ukraine** war
- the **Hormuz Strait** conflict between the US, Iran, and Gulf states

## Pipeline

```
News feeds
  → semantic extraction
  → claim extraction
  → evidence graph
  → factor identification
  → competing hypotheses
  → multi-LLM debate
  → confidence estimates
  → predictions / scenario analysis
```

## Factors as explicit variables

Rather than burying signals in prose, the system extracts underlying factors such as:

- troop movements
- logistics
- ammunition consumption
- industrial production
- sanctions
- diplomatic signalling
- satellite imagery
- historical precedents
- economic indicators
- political incentives
- military doctrine

## LLM debate questions

Models debate:

- Which reports corroborate each other?
- Which conflict?
- Which appear propagandistic?
- Which assumptions drive disagreement?
- Which conclusions are strongly supported?
- Which remain speculative?

## Relationship to Milcah

Milcah is fundamentally an **argument-evaluation engine**, not a chatbot — which
fits this domain naturally. Valhalla schedules Milcah for the debate layer;
Hanani supplies the geopolitical corpus, factor taxonomy, and synthesis policies.

## Platform relationship

```
Valhalla (orchestration)
    ├── Milcah   — multi-LLM debate, argument evaluation
    ├── Tirzah   — memory over ingested reports
    ├── Hoglah   — LLM execution queue
    └── Galeed   — process trace
         └── Hanani (this repo) — news corpus + factor taxonomy
```

Scripture translation is a **separate specialised instance**: Ed.