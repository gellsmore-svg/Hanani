# Hanani Living Semantic Model / Ontology

**Version:** 0.3
**Graph ID:** `mechanism`
**Status:** Seed graph — expandable from scholarly mechanisms, not from news cycles  
**Project:** Hanani **reasoning system** (see [`reasoning-system.md`](../reasoning-system.md))  
**Role:** **Graph A** — mechanism/factor semantics for **Layer 2** atom tagging  

This document is **not** a one-off conflict analysis. It is the living, versioned
backbone that logic atoms attach to after passing **Layer 1** rhetorical assessment
([`rhetorical-logic-graph.md`](rhetorical-logic-graph.md)).

---

## 0. Operating principles (non-negotiable)

| Principle | Enforcement |
|---|---|
| Rhetorical logic first | No atom extraction until source passes logic audit |
| Reputation-blind | Outlet size, funding, fame, corpus associations are **ignored** in audit and tagging |
| Exhaustive application | Every atom receives multi-layer tags with step-by-step justification |
| Living model | Changelog + inference notes track stability vs. shift |
| Neutrality on moral verdicts | Mechanisms, evidence, framework — not ideological closure |
| Bias countermeasure | Explicitly flag when default LLM associations are suppressed |

**Default tendency countered:** probabilistic summarization, 1–2 tag shortcuts, prestige-based source acceptance.

---

## 1. Position in the reasoning engine

```
Logic atom → Layer 1 (rhetoric graph) → Layer 2 (this mechanism graph) → assessment record
                                                                    ↓
                                              [later] collective narrative + outcomes
```

## 2. Workflow (when sources are eventually ingested)

```mermaid
flowchart TD
  A[Initialize / update ontology] --> B[Source ingestion]
  B --> C{Rhetorical logic audit}
  C -->|Weak| D[Set aside + reason]
  C -->|Strong / qualified Moderate| E[Logic atom extraction]
  E --> F[Exhaustive multi-layer tagging]
  F --> G[Analysis graph construction]
  G --> H[Gap analysis]
  H --> I[Active retrieval if needed]
  I --> B
  G --> J[Ontology update + version bump]
  J --> K[Structured cycle output]
```

1. Initialize or update living ontology (this document).
2. Source ingestion → rhetorical logic filter (mandatory).
3. Logic atom extraction (robust sources only).
4. Exhaustive tagging per atom (all applicable layers).
5. Analysis graph (atoms, sources, concepts, edges).
6. Gap analysis vs. full ontology.
7. Active retrieval → same filter on new material.
8. Ontology update, changelog, stability notes.
9. Structured cycle output (audit, atoms, graph, gaps, correlations).

---

## 2. Rhetorical logic audit criteria

Apply to **every** source before atom extraction. Output audit block first.

| Criterion | Questions |
|---|---|
| **Chain completeness** | Are premises, warrants, and axioms explicit? List enthymemes that would collapse the argument if false. |
| **Evidence integration** | How is evidence weighed? Are counter-explanations and disconfirming evidence considered? |
| **Qualifiers & falsifiability** | Scope conditions, uncertainty, openness to being wrong? |
| **Analytical intent vs. closure** | Causal/mechanistic insight vs. narrative/ideological closure with missing steps? |
| **Update signals** | Willingness to revise with new information or strong counter-reasoning? |

**Qualification scale**

| Score | Proceed to atoms? |
|---|---|
| **Strong** | Yes |
| **Moderate** | Yes, with explicit gaps listed |
| **Weak** | No — set aside with reasons |

```json
{
  "audit_id": "AUDIT-YYYYMMDD-NNN",
  "source_ref": "opaque id — not outlet prestige",
  "robustness": "Strong | Moderate | Weak",
  "enthymemes": ["..."],
  "gaps": ["..."],
  "reputation_ignored": true
}
```

---

## 3. Logic atom schema

```json
{
  "atom_id": "Atom-001",
  "source_ref": "AUDIT-...",
  "text": "verbatim or tight paraphrase of the claim",
  "type": "assertion | causal_claim | analogy | intent_assessment | counterfactual | warrant | premise",
  "layers": ["L1.anarchy", "L3.prospect_loss_aversion"],
  "cross_cutting": ["schelling_focal_point"],
  "historical_anchors": ["cuban_missile_crisis"],
  "tag_justification": "step-by-step link text → ontology element",
  "evidence_for": ["..."],
  "evidence_against": ["..."],
  "alternatives": ["..."],
  "strength": "high | medium | low",
  "uncertainty": "explicit note",
  "speed_differential": {
    "side_a_processing": "fast | slow | unknown",
    "side_b_processing": "fast | slow | unknown",
    "differential_exploited": "A_faster | B_faster | parity | none_evident",
    "probe_intent": "measure_reaction_speed | measure_model_precision | deliberate_ambiguity | none_evident",
    "notes": "mandatory — use 'none evident' explicitly if no speed signal"
  }
}
```

---

## 4. Layer 1 — Superstructure / foundational structural

*Load-bearing constraints, incentives, and possibilities. Architecture that limits what coalitions and leaders can sustain.*

### 4.1 International anarchy & security dilemma

- **Definition:** No supreme authority; self-help; one actor's security measures reduce others' security (security dilemma).
- **Tag when:** Arguments hinge on relative power, defensive vs. offensive ambiguity, arms/buildup spirals without central enforcement.
- **Inference notes (v0.1):** *Seed only — no theatre-specific inference yet.*

### 4.2 Power distribution / polarity & shifts

- Unipolar / bipolar / multipolar frames; relative capability trajectories; alliance aggregation effects.
- **Tag when:** Balance-of-power claims, hegemonic restraint/overstretch, coalition feasibility.

### 4.3 Nuclear deterrence architecture & MAD logic

- Civilization-scale Chicken; escalation ladders; tactical vs. strategic distinction; commitment problems at the nuclear threshold.
- **Tag when:** Nuclear rhetoric, escalation dominance, damage-limitation vs. assured retaliation logic.

### 4.4 Economic interdependence, sanctions, trade networks, kleptocratic revenue

- Trade weaponization, energy rents, sanctions evasion, elite extraction models feeding war budgets.
- **Tag when:** Economic statecraft, resource curse, sanctions impact chains, corruption–war finance links.

### 4.5 Geographic / strategic fundamentals

- Chokepoints (Hormuz, straits), depth, interior lines, buffer zones, demographic/economic base.
- **Tag when:** Terrain/logistics/geography treated as binding constraints on strategy.

### 4.6 Cross-cutting: Schelling mixed-motive games

- Simultaneous cooperation/competition; bargaining embedded in conflict.
- **Tag when:** Compellence + accommodation mixed; "negotiate while fighting" structure.

---

## 5. Layer 2 — Mid-level processual / institutional / coalitional

*How states and regimes process decisions through institutions, coalitions, and path-dependent structures.*

### 5.1 Selectorate theory & winning coalition size

- Small coalitions → private goods, higher risk tolerance in foreign policy; personalist rule dynamics.
- **Tag when:** Elite patronage, coup-proofing, purge cycles, foreign adventure as domestic rent distribution.

### 5.2 Two-level games (Putnam)

- International bargaining simultaneous with domestic ratification / coalition maintenance.
- **Tag when:** Leader must sell foreign policy at home; domestic audience costs constrain international offers.

### 5.3 Bureaucratic politics & organizational processes

- Standard operating procedures, inter-service rivalry, information stovepipes, incrementalism.
- **Tag when:** "Where you stand depends on where you sit"; organizational outputs ≠ rational unitary actor.

### 5.4 Information / narrative control ecosystems & propaganda

- State media, censorship, bot networks, legal pressure on dissent — as **institutional systems**, not moral labels.
- **Tag when:** Information environment shapes what elites and publics can believe or say.

### 5.5 Path dependence & critical junctures

- Early choices constrain later option sets; contingent events lock in trajectories.
- **Tag when:** "Once X happened, Y range collapsed" — Crimea, Maidan, JCPOA exit, etc. as junctures.

### 5.6 Cross-cutting: Putnam-style entanglement

- Domestic politics entangled with international negotiation games (ratification, two-audience problem).

---

## 6. Layer 3 — Agentic / psychological / cognitive

*Leader and decision-maker cognition — can dominate in personalist systems.*

### 6.1 Prospect theory & loss aversion

- Reference-dependent utility; risk-seeking in losses domain; risk-averse in gains; reference points (status, identity, historical grievance).
- **Tag when:** "Cannot afford to lose face/territory/influence"; gamble to recover losses; sunk-status fights.

### 6.2 Cognitive biases & heuristics

- Overconfidence, confirmation, escalation of commitment, motivated reasoning, availability.
- **Tag when:** Doubling down, ignoring disconfirming intel, analogy-driven leaps.

### 6.3 Personality & Dark Triad (evidence-gated)

- Narcissism/grandiosity, Machiavellianism, low-empathy patterns — **only where text supplies behavioral evidence**, not pop psychology.

### 6.4 Emotional / motivational drivers

- Paranoia, revanchism, honor/revenge, need for control/infallibility.

### 6.5 Mental simulation, counterfactuals & scenario planning

- Internal role-play of hypotheticals; war-gaming rhetoric; pre-mortems stated or implied.

### 6.6 Perception & misperception (Jervis)

| Model | Core mechanism |
|---|---|
| **Spiral** | Defensive actions misread as aggressive → escalation via security dilemma |
| **Deterrence** | Adversary assumed inherently aggressive; credible threats required |
| **Cognitive consistency** | New info assimilated to existing images |
| **Overestimation of influence** | Own signals assumed more controlling than they are |
| **Shared worldview error** | Assuming adversary shares your frame |

- **Tag when:** Intent attribution, misreading mobilization, mirror-imaging, attribution errors.

### 6.7 Cross-cutting: Historical analogies (often misapplied)

- Munich, Cuba, Afghanistan, etc. used as warrants — tag analogy **and** assess misapplication risk.

---

## 7. Layer 4 — Communicative / signaling layer

*Expressive and manipulative surface — what is said vs. what is costly.*

### 7.1 Cheap talk vs. costly signaling (Fearon / Schelling)

- Credibility from sunk costs, tying hands, observable military/industrial moves vs. rhetoric alone.
- **Tag when:** Threats, promises, mobilization announcements, sanctions "deadlines."

### 7.2 Madman theory / unpredictability postures

- Cultivated irrational image for brinkmanship leverage (Nixon tradition and extensions).

### 7.3 Brinkmanship & escalation dominance signaling

- Chicken dynamics; who swerves; controlled escalation as bargaining.

### 7.4 Audience targeting

- Domestic rally vs. international deterrence vs. ally reassurance — same act, multiple audiences.

### 7.5 Propaganda, narrative warfare & moral disengagement

- Framing, dehumanization, victimhood narratives — as **mechanisms**, not truth adjudication.

### 7.6 Cross-cutting: Schelling focal points

- Salient coordination solutions in tacit bargaining (explicit lines, calendar dates, symbolic places).

### 7.7 Cross-cutting: Credible commitments

- Mechanisms making threats/promises believable despite reneging incentives (tripwires, treaty law, audience costs).

---

## 8. Layer 5 — Emergent / dynamic / complex adaptive

*Interactions and feedback over time — pathologies and emergent structures.*

### 8.1 Active game structures

| Game | Mechanism | Tag when |
|---|---|---|
| Prisoner's Dilemma | Mutual defection trap | Sanctions races, verification breakdowns |
| Chicken | Brinkmanship, swerve | Crises, Hormuz incidents, nuclear shadow |
| Repeated games | Reputation, tit-for-tat | Long-running rivalries, ceasefire patterns |
| Focal points | Tacit coordination | Red lines, straits, symbolic dates |

### 8.2 Feedback loops & spirals

- Rhetoric → perception → counter-action → updated assessments; L1 dilemma + L3 loss domain + L4 signals.

### 8.3 Face-saving, cognitive dissonance & "punish before accept"

- Need for costs inflicted or partial victory to justify exit; domestic audience costs.

### 8.4 Path dependence, lock-in, hubris cycles & overreach

- Napoleonic / WWII eastern front patterns as **structural** cautionary anchors — tag mechanism, not analogy alone.

### 8.5 Structural enablement of personalist pathology

- Small coalitions reward intrigue; loyalty games; complexity addiction.

### 8.6 Moral / ethical emergence & inhumane outcomes

- How layers combine to enable population-disregard while "rational" for narrow selectorate — descriptive, not prescriptive.

### 8.7 Cross-cutting: Jervis spiral vs. deterrence in real time

- Same observable act read through different images → different recommended responses.

### 8.8 Cross-cutting: Schelling commitment problems in ongoing interactions

- Promises erode; audience costs decay; new crises require re-establishing credibility.

### 8.9 Cross-cutting dynamic: Asymmetric Sensemaking Speed & Informational Brinkmanship (ASSSIB)

**Canonical name:** `asymmetric_sensemaking_speed_informational_brinkmanship`  
**Primary layer:** L5 (emergent) — **cross-cuts** L3 (Jervis, prospect theory, mental simulation speed), L4 (cheap talk, ambiguity, probing signals), L2 (two-level domestic processing speeds, selectorate cohesion), L1 (security dilemma under time pressure).

**Definition:** Deliberate or emergent probing, ambiguity creation, and information maneuvers whose primary target is the **relative speed, precision, and coherence** with which actors detect ambiguous signals, process them through an internal model, update assessments, coordinate responses, and avoid over- or under-reaction — and the **exploitation of differentials** in that processing speed.

| Feature | Codification |
|---|---|
| Low-cost probing | Extreme rhetoric, leaks, sensationalism, or minor moves test alliance weak spots and **reaction speed/precision** — not necessarily literal intent to execute the threatened action |
| Human + strategic stress | "Throwaway" extreme statements as stress response **and** probe in murky information environments |
| Differential risk | Danger from **gaps in processing speed/quality** between sides — not absolute speed alone |
| Ambiguity as weapon | Deliberate vagueness slows opponent coherent response; buys time for prober |
| Murky sensory brinkmanship | Cat-and-mouse in **sensemaking** domain, not only military moves |
| Traffic metaphor | Systemic collision risk from speed mismatch (harmony/disruption) even without intent to collide |
| Hanani advantage | Side applying richer systematic model **faster** gains edge; single-layer slow sensemaking = vulnerability |

**Layer linkages:**

| Linked concept | Interaction |
|---|---|
| Jervis misperception | Amplified under time pressure; spiral/deterrence reads made before models converge |
| Prospect theory | Loss-domain actors more probe-prone **and** more vulnerable to being slowed |
| Schelling | Incomplete-info probing; focal points under ambiguity; credible-commitment **tests** |
| Two-level games | Domestic sensemaking speed vs. international coordination lag |
| Selectorate | Cohesion/speed of winning coalition affects collective processing |
| Feedback loops (8.2) | Probe → misread → partial response → escalatory probe |

**Tagging guidance (mandatory per atom):**

1. Does the atom assume **fast or slow** sensemaking on Side A or Side B?
2. Is probing intended to measure **reaction speed**, **model precision**, or **create ambiguity**?
3. If none evident — record **`none_evident`** explicitly (counts as gap signal).
4. Tag ASSSIB when any probe, leak, sensational framing, or coordination-lag claim appears.

**Graph edges (analysis graph):**

- `processes_faster_than` (actor → actor, on atom or probe)
- `probes_sensemaking_speed` (signal → target alliance/actor)
- `creates_ambiguity_to_slow` (signal → target processing)
- `exploits_speed_differential` (actor → actor)

### 8.9b Coherence speed vs. raw reaction speed

**Distinction:** Reaction speed alone is insufficient for collective actors. A fast but
**fragmented** alliance may still present a **slow, incoherent** effective response to a
probe. Hanani tracks both dimensions per party:

| Dimension | Values | Meaning |
|---|---|---|
| `reaction_speed` | `fast` / `slow` / `unknown` | How quickly the party detects, models, and initiates response |
| `coherence` | `high` / `medium` / `low` / `fragmented` / `unknown` | Internal model alignment and cross-unit coordination quality |

**Source history linkage:** Profiles **shall** be grounded in per-source **article history**
(`SourceCorpus`) — a temporal sequence of witnesses, not a single headline snapshot.
Trajectory shifts (e.g. alliance coherence degrading across three articles from one source)
are first-class signals for interpreting **current moves**.

**Individual parties:** states, leaders, agencies — each maintains a `CoherenceSpeedProfile`
with an observation trajectory keyed to `source_id`, `article_id`, optional `atom_id`.

**Collective parties — LCD constraint:** Alliances, unions, and coalitions **shall** expose
a `CollectiveCoherenceProfile` where effective capability is bounded by the
**lowest common denominator (LCD)** member:

| LCD field | Rule |
|---|---|
| `lcd_reaction_speed` | No faster than the **slowest** member |
| `lcd_coherence` | No higher than the **least coherent** member |
| `lcd_speed_member` / `lcd_coherence_member` | Explicit binding member ids |

**ASSSIB move interpretation:** When a probe targets a collective, assess whether the prober
exploits the **LCD binding member** (coordination lag, national narrative fragmentation)
rather than assuming unitary-actor speed. `move_context()` ties atom-level
`speed_differential` blocks to collective LCD profiles.

**Graph edges (coherence):**

- `constrains_collective_speed` (member → collective)
- `constrains_collective_coherence` (member → collective)
- `lcd_binding_member` (member → collective LCD field)
- `observed_in_article` (observation → article in source history)
- `profile_trajectory` (party → time-ordered observations)

---

## 8.10 Integration summary — ASSSIB (v0.2)

ASSSIB makes **sensemaking speed** a first-class analytical object. The core risk is often not the threatened action itself but a **dangerous mismatch** in how quickly and coherently each side interprets probes.

**Why Hanani value increases:** Applying the full layered ontology systematically and faster than an opponent (or than one's own prior cycle) is a **strategic capability** — it reduces vulnerability to informational brinkmanship and improves probe interpretation (distinguishing cheap talk + stress from costly commitment).

**Workflow hooks:** Rhetoric audits flag speed/ambiguity language; Layer 2 tags ASSSIB + linked layers; gap analysis asks about actor processing differentials; retrieval prioritizes reaction-time and sensemaking-quality evidence.

**v0.3 addition:** Per-source article histories feed individual coherence trajectories;
collective LCD profiles constrain interpretation of alliance/coalition responses to probes.

---

## 8.11 Tagging examples (hypothetical logic atoms)

**Example A — Atom-HYP-001**  
*"A Baltic frontline state official's leaked memo suggesting maximalist aid demands is intended to test whether NATO/EU capitals coordinate a precise response within 48 hours or fragment into national narratives."*

| Field | Assessment |
|---|---|
| Layers | L4.cheap_talk, L2.two_level_games, L5.ASSSIB |
| Speed differential | Side A (alliance capitals): slow/fragmented vs. Side B (prober): fast — **differential exploited by prober** |
| Probe intent | `measure_reaction_speed` + `measure_model_precision` |
| Jervis | Spiral risk if leak read as unified alliance intent |

**Example B — Atom-HYP-002**  
*"Leader's televised ultimatum deadline is rhetorically extreme but troop indicators show no matching costly mobilization — analysts should treat primarily as domestic stress discharge and international probe, not imminent execution."*

| Field | Assessment |
|---|---|
| Layers | L4.cheap_talk vs costly signal, L3.prospect_loss_aversion, L5.ASSSIB |
| Speed differential | Opponent slow processors may **over-react** to cheap talk; fast processors gain calibration time |
| Probe intent | `deliberate_ambiguity` + `measure_model_precision` |

**Example C — Atom-HYP-003**  
*"ExComm-style meetings during the missile crisis compressed sensemaking into hours; back-channel parallel processing reduced public-deadline pressure."*

| Field | Assessment |
|---|---|
| Layers | L2.bureaucratic_politics, L5.ASSSIB, L4.credible_commitments |
| Speed differential | US **accelerated** coherent processing via parallel channels; reduced speed mismatch with Soviet probes |
| Anchor | `cuban_missile_crisis_1962` |

---

## 9. Historical anchors (seed mappings)

*Use for cross-linking atoms — not as substitutes for evidence in new texts.*

### 9.1 Cuban Missile Crisis (1962)

| Layer | Illustrative mechanisms |
|---|---|
| L1 | Nuclear Chicken; bipolar competition |
| L2 | ExComm bureaucratic politics; alliance consultation |
| L3 | Misperception management; stress under uncertainty |
| L4 | Naval quarantine as costly signal; back-channel cheap talk |
| L5 | Brinkmanship resolution; focal point (missile trade); spiral avoided via direct communication |
| **ASSSIB** | Time-compressed sensemaking; parallel back-channels reduced speed mismatch under probes |

### 9.2 Russia–Ukraine (2014 → 2022+)

| Layer | Illustrative mechanisms (hypothesis templates — verify per source) |
|---|---|
| L1 | Security dilemma; energy interdependence; sanctions architecture |
| L2 | Small-coalition / personalist incentives; domestic narrative ratification |
| L3 | Prospect losses (influence, NATO/EU expansion frames); historical identity reference points |
| L4 | Troop buildups as costly signals vs. ultimatum rhetoric as cheap talk |
| L5 | Path dependence from Crimea/Minsk; escalation spirals; commitment problems on ceasefires |
| **ASSSIB** | Troop-buildup probes vs. rhetoric; alliance coordination speed on aid/red lines |

### 9.3 Baltic / alliance probe pattern (template)

| Layer | Mechanism |
|---|---|
| L2 | Frontline state two-level pressure on alliance capitals |
| L4 | Leaks / extreme framing as cheap-talk probes |
| L5 **ASSSIB** | Tests NATO/EU **reaction speed and precision** — not necessarily literal intent behind leak content |

### 9.4 Napoleonic overextension (lighter anchor)

| Layer | Mechanism |
|---|---|
| L5 | Hubris cycle; logistics–ambition mismatch; coalition aggregation |
| L3 | Overconfidence; escalation of commitment |
| L6 | Misperception of Russian winter campaign capacity (historical analogy risk) |

### 9.5 Hormuz / Gulf chokepoint (theatre anchor — seed)

| Layer | Mechanism |
|---|---|
| L1 | Geographic chokepoint; energy market interdependence |
| L4 | Mine/threat rhetoric vs. actual interdiction costs |
| L5 | Chicken dynamics; repeated incident games |

---

## 10. Analysis graph (empty at v0.1)

**Node types:** `logic_atom`, `source`, `ontology_concept`, `historical_anchor`  
**Edge types:** `agrees`, `contradicts`, `complements`, `implies`, `gap`, `supports`, `weakens`, `processes_faster_than`, `probes_sensemaking_speed`, `creates_ambiguity_to_slow`, `exploits_speed_differential`

```mermaid
graph LR
  subgraph pending [Awaiting first ingestion cycle]
    O[Ontology v0.1]
    G[Empty graph]
  end
  O -.-> G
```

*Adjacency list and populated Mermaid will appear after first source cycle.*

---

## 11. Initial gap inventory (pre-sources)

| Priority | Gap | Resolution need |
|---|---|---|
| High | No atoms for Russia–Ukraine theatre | Ingest robust analytical sources |
| High | No atoms for Hormuz theatre | Same |
| High | Layer 3 Jervis models untested on live text | Audited sources with intent/misperception claims |
| Medium | Kleptocratic revenue (L1.4) unpopulated | Economic / sanctions analysis with explicit chains |
| Medium | Bureaucratic politics (L2.3) thin | ExComm-style organizational accounts |
| Low | Dark Triad tags | Only if behavioral evidence in text — avoid seeding from reputation |
| **High** | ASSSIB speed-differential tags on live atoms | Sources on alliance coordination lag, probe/leak dynamics |
| **High** | Per-party coherence trajectories from source histories | Multi-article sequences per source; collective LCD binding members |

---

## 12. Changelog

### v0.3 — 2026-07-10 (coherence speed profiles + LCD)

- Added §8.9b: coherence vs. raw reaction speed; source-history trajectories; collective LCD constraint.
- New registry constants: `COHERENCE_LEVELS`, `PARTY_TYPES`, `COHERENCE_GRAPH_EDGES`.
- `SpeedDifferentialAssessment` extended with per-side coherence and optional party ids.
- Scaffold modules: `hanani.sources.SourceCorpus`, `hanani.coherence.CoherenceRegistry`.
- **Stability:** ASSSIB §8.9 unchanged; L1–L4 seeds unchanged.
- **Next:** Wire profile updates into ingestion workflow; populate live trajectories from atoms.

### v0.2 — 2026-07-05 (ASSSIB integration)

- Added **Asymmetric Sensemaking Speed & Informational Brinkmanship** as prominent L5 cross-cutting dynamic (§8.9).
- Mandatory `speed_differential` block on logic atom schema; new analysis-graph edge types.
- Integration summary (§8.10), three hypothetical tagging examples (§8.11).
- Historical anchors updated: Cuba ASSSIB row; Ukraine ASSSIB row; Baltic/alliance probe template (§9.3).
- **Stability:** L1–L4 seed concepts unchanged.
- **Inference:** ASSSIB is structural addition — no theatre inference until atoms ingested.
- **Next:** Process sources with augmented mandatory speed assessment.

### v0.1 — 2026-07-05 (initialization)

- Created five-layer ontology with cross-cutting concepts (Schelling, Jervis, Putnam).
- Defined rhetorical logic audit schema, logic atom JSON shape, analysis graph edge types.
- Seeded historical anchors: Cuban Missile Crisis, Russia–Ukraine arc, Napoleonic overextension, Hormuz chokepoint template.
- **Stability:** N/A (first version).  
- **Inferences:** None — no source atoms yet.  
- **Next:** Await first source text(s); run full workflow cycle.

---

## 13. Inference notes

*No live inferences. This section records shifts when multiple atoms support updating default reference points, coalition models, or spiral/deterrence readings.*

| Inference ID | Status | Layers | Evidence atoms | Version impact |
|---|---|---|---|---|
| — | — | — | — | — |

---

## 14. Relation to Hanani factors

Hanani's operational factor list (`hanani factors`) captures **observable variables** (troops, logistics, sanctions, etc.). This ontology captures **analytical mechanisms** (why variables matter). Atoms should tag **both** where applicable:

| Factor (operational) | Typical ontology layers |
|---|---|
| troop-movements | L1, L4, L5 |
| diplomatic-signalling | L4, L2 |
| propaganda-signals | L2.4, L4.5 |
| political-incentives | L2.1, L3.1 |
| historical-precedent | L3.7, §9 anchors |

---

*End of Living Semantic Model v0.3*