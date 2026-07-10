# Rhetorical Logic Semantic Graph

**Version:** 0.1  
**Graph ID:** `rhetoric`  
**Purpose:** Layer 1 truth assessment — evaluate sources and logic atoms by **reasoning
structure in the text**, not outlet reputation.

---

## 1. Graph role in Hanani

| Layer | Graph | Question |
|---|---|---|
| **Layer 1** | This graph | Is the argument structurally sound? Any fallacies, enthymemes, closure? |
| **Layer 2** | Mechanism graph | What geopolitical mechanisms does the content engage? |

Nodes here are **patterns to detect**, not moral judgments. A hit on `cherry_picking`
does not mean "bad outlet" — it means the **quoted reasoning** selects confirming
evidence without addressing disconfirmation.

---

## 2. Node taxonomy

### 2.1 Audit criteria (source-level and atom-level)

| Node ID | Description |
|---|---|
| `audit.chain_completeness` | Premises, warrants, conclusion traceable |
| `audit.evidence_integration` | Counter-evidence weighed |
| `audit.qualifiers_falsifiability` | Scope, uncertainty, testable claims |
| `audit.analytical_intent` | Mechanism-seeking vs. narrative closure |
| `audit.update_signals` | Revision openness |

### 2.2 Argument structure roles

| Node ID | Role |
|---|---|
| `arg.premise` | Stated or enthymematic input |
| `arg.warrant` | Bridge premise → conclusion |
| `arg.conclusion` | Claim drawn |
| `arg.qualifier` | Scope/limitation |
| `arg.rebuttal` | Acknowledged objection |
| `arg.enthymeme` | Load-bearing unstated assumption |

### 2.3 Robustness tiers

| Node ID | Admissible for mechanism inference? |
|---|---|
| `robust.strong` | Yes |
| `robust.moderate` | Yes, with documented gaps |
| `robust.weak` | No (store optionally, exclude from synthesis) |

---

## 3. Fallacy & pattern nodes (exhaustive seed)

Organized for **geopolitical analytical text**. Expand only with pattern evidence.

### 3.1 Formal / structural

| Node ID | Pattern |
|---|---|
| `fallacy.affirming_consequent` | If A then B; B; therefore A |
| `fallacy.denying_antecedent` | If A then B; not A; therefore not B |
| `fallacy.false_dilemma` | Only two options when more exist |
| `fallacy.equivocation` | Key term shifts meaning mid-argument |
| `fallacy.circular_reasoning` | Conclusion assumed in premise |

### 3.2 Evidence & generalization

| Node ID | Pattern |
|---|---|
| `fallacy.cherry_picking` | Confirming evidence only |
| `fallacy.hasty_generalization` | Broad claim from thin sample |
| `fallacy.anecdotal` | Single story → general law |
| `fallacy.survivorship_bias` | Visible successes; invisible failures |
| `fallacy.base_rate_neglect` | Ignores prior probability |
| `fallacy.post_hoc` | Sequence mistaken for causation |

### 3.3 Causal & mechanistic

| Node ID | Pattern |
|---|---|
| `fallacy.single_cause` | One factor explains complex outcome |
| `fallacy.slippery_slope` | Unwarranted escalation chain |
| `fallacy.false_balance` | Two sides equally supported when evidence asymmetric |
| `fallacy.teleology` | Outcome assumed inevitable from narrative arc |

### 3.4 Authority & attribution (text-only — reputation-blind)

| Node ID | Pattern |
|---|---|
| `fallacy.appeal_to_authority_in_text` | Conclusion rests on cited title/institution **in the argument**, not model prior |
| `fallacy.ad_hominem_in_text` | Attacks actor not claim **as stated in text** |
| `fallacy.genetic` | Dismisses claim by origin alone **in text** |
| `fallacy.motivated_skepticism` | Asymmetric standards for confirming vs. disconfirming |

### 3.5 Geopolitical / analytical specific

| Node ID | Pattern |
|---|---|
| `fallacy.mirror_imaging` | Assumes adversary shares own values/calculus |
| `fallacy.analogy_misuse` | Historical analogy as warrant without mechanism match |
| `fallacy.capability_intent_conflation` | Capacity → intent without intermediate reasoning |
| `fallacy.rhetoric_action_conflation` | Cheap talk treated as costly signal without evidence |
| `fallacy.unitary_actor` | State/leaders as single rational unit ignoring bureaucracy |
| `fallacy.presentism` | Past actors judged anachronistically without warrant |
| `fallacy.narrative_closure` | Story completeness substituted for causal proof |

### 3.6 Enthymeme templates (load-bearing gaps)

| Node ID | Typical unstated assumption |
|---|---|
| `enthymeme.risk_neutral_adversary` | Opponent maximizes same utility function |
| `enthymeme.static_preferences` | Preferences don't shift with losses/gains |
| `enthymeme.credible_threat_assumed` | Threat believed without commitment mechanism |
| `enthymeme.domestic_unified` | Leader speaks for all domestic veto players |
| `enthymeme.linear_escalation` | Escalation ladder fixed and shared |

---

## 4. Edge types

| Edge | Meaning |
|---|---|
| `subtype_of` | Fallacy specialization |
| `violates` | Atom/source instantiates fallacy |
| `exhibits` | Partial match / qualified hit |
| `missing_warrant` | Enthymeme gap breaks chain |
| `supports_chain` | Warrant legitimately links premise → conclusion |
| `undermines` | Rebuttal or counter-evidence present |
| `detected_in` | Pattern found in atom `X` or source `Y` |
| `contradicts` | Two rhetoric assessments incompatible |

---

## 5. Layer 1 assessment algorithm (spec)

For each logic atom `a`:

1. **Segment** into premise/warrant/conclusion candidates.
2. **Match** against fallacy & enthymeme nodes (exhaustive scan — all categories).
3. **Score** audit criteria nodes (boolean + notes).
4. **Aggregate** to `robust.strong | moderate | weak`.
5. **Emit** `rhetoric_assessment` with every hit listed (no silent drops).
6. **Set** `admissible_for_inference` from robustness tier.

Reputation, outlet size, and training-data associations are **not inputs** to step 2–4.

---

## 6. Changelog

### v0.1 — 2026-07-05

- Initialized audit criteria, argument roles, robustness tiers.
- Seeded 25+ fallacy/pattern nodes + 5 enthymeme templates.
- Defined edge types and Layer 1 assessment spec.

**Next:** Wire to `hanani.rhetoric` module and `hanani.reasoning.layer1` implementation.