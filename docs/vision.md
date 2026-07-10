# Vision — Geopolitical News Reasoning System

Standalone project — no shared platform layer with scripture translation or any
other application.

## What this is

A **reusable reasoning system** — not a one-off briefing on a current crisis.

It maintains **two expandable semantic graphs** (mechanisms + rhetorical logic), evaluates
every **logic atom** through layered checks, and (later) synthesises a collective
narrative with likely outcomes.

> What do all available reports imply when combined?

See [`reasoning-system.md`](reasoning-system.md).

## Initial theatres

- Russia–Ukraine
- Hormuz Strait / US–Iran–Gulf states

## Pipeline

```
News feeds → semantic extraction → claim extraction → evidence graph
  → factor identification → competing hypotheses → multi-LLM debate
  → confidence estimates → predictions / scenario analysis
```

## Factors as explicit variables

Troop movements, logistics, ammunition, industrial production, sanctions,
diplomatic signalling, satellite imagery, historical precedents, economic
indicators, political incentives, military doctrine, propaganda signals.

## Living semantic ontology

Multi-layer analytical model (rhetorical logic first, reputation-blind):
[`docs/ontology/living-semantic-model.md`](ontology/living-semantic-model.md) v0.1.

Operational factors (`hanani factors`) capture observable variables; the ontology
captures mechanisms (security dilemma, prospect theory, signaling, spirals, etc.).

## Milcah

Milcah is the argument-evaluation and multi-LLM debate layer — scheduled by
Hanani's internal workflow orchestration (`hanani.workflow`).