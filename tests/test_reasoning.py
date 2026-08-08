from hanani.graph import SemanticGraph, seed_mechanism_nodes, seed_rhetoric_nodes
from hanani.reasoning import LogicAtom, ReasoningEngine, default_engine
from hanani.rhetoric import FALLACIES, admissible_for_inference, list_fallacies


def test_rhetoric_graph_has_fallacies() -> None:
    assert len(list_fallacies()) >= 20
    assert "fallacy.cherry_picking" in FALLACIES


def test_admissible_tiers() -> None:
    assert admissible_for_inference("Strong")
    assert admissible_for_inference("robust.moderate")
    assert not admissible_for_inference("Weak")


def test_layer1_blocks_layer2_on_weak_rhetoric() -> None:
    engine = ReasoningEngine()
    atom = LogicAtom(atom_id="a1", source_id="s1", text="claim")
    layer1 = engine.assess_layer1(atom, rhetoric_hits=["fallacy.cherry_picking"])
    assert layer1.robustness == "Weak"
    assert engine.assess_layer2(atom, layer1) is None


def test_layer1_audit_scores_are_unassessed_not_true() -> None:
    """Review H2: scaffold must not write fabricated True audit passes."""
    from hanani.rhetoric import AUDIT_CRITERIA

    engine = ReasoningEngine()
    atom = LogicAtom(atom_id="a1", source_id="s1", text="A clean factual claim.")
    layer1 = engine.assess_layer1(atom, rhetoric_hits=[])
    assert set(layer1.audit_scores) == set(AUDIT_CRITERIA)
    assert all(v is None for v in layer1.audit_scores.values())


def test_full_pipeline_strong_atom() -> None:
    engine = default_engine()
    atom = LogicAtom(atom_id="a1", source_id="s1", text="Mobilization preceded talks.")
    record = engine.assess_atom(
        atom,
        mechanism_tags=["L4.cheap_talk_costly_signaling"],
        justifications={"L4.cheap_talk_costly_signaling": "text distinguishes rhetoric from moves"},
    )
    assert record.layer1 is not None
    assert record.layer1.admissible_for_inference
    assert record.layer2 is not None
    assert record.layer2.tags


def test_seed_graphs() -> None:
    from hanani.ontology import LAYERS

    mg = seed_mechanism_nodes(LAYERS)
    rg = seed_rhetoric_nodes(FALLACIES, {})
    assert len(mg.nodes_by_kind("mechanism")) > 30
    assert len(rg.nodes_by_kind("rhetoric")) >= 20


def test_asssib_in_ontology_and_speed_assessment() -> None:
    from hanani.ontology import CROSS_CUTTING_DYNAMICS, LAYERS
    from hanani.reasoning import LogicAtom, SpeedDifferentialAssessment, default_engine

    assert "asymmetric_sensemaking_speed_informational_brinkmanship" in CROSS_CUTTING_DYNAMICS
    assert "asymmetric_sensemaking_speed_informational_brinkmanship" in LAYERS["L5_emergent_dynamic"]

    atom = LogicAtom(
        atom_id="a1",
        source_id="s1",
        text="A leaked memo probes whether the alliance can coordinate a precise reaction within 48 hours.",
    )
    record = default_engine().assess_atom(
        atom,
        speed=SpeedDifferentialAssessment(
            side_a_processing="slow",
            side_b_processing="fast",
            differential_exploited="B_faster",
            probe_intent="measure_reaction_speed",
            notes="alliance coordination lag implied",
        ),
    )
    assert record.layer1 is not None
    assert record.layer1.sensemaking_signals
    assert record.layer2 is not None
    assert "asymmetric_sensemaking_speed_informational_brinkmanship" in record.layer2.tags
    assert record.layer2.speed_differential.probe_intent == "measure_reaction_speed"


def test_speed_differential_coherence_fields() -> None:
    from hanani.reasoning import SpeedDifferentialAssessment

    speed = SpeedDifferentialAssessment(
        side_a_coherence="fragmented",
        side_b_coherence="high",
        side_a_party_id="party-a",
    )
    assert speed.side_a_coherence == "fragmented"
    assert speed.side_a_party_id == "party-a"


def test_semantic_graph_neighbors() -> None:
    g = SemanticGraph()
    from hanani.graph import GraphEdge, GraphNode

    g.add_node(GraphNode(id="a", kind="logic_atom", label="atom"))
    g.add_node(GraphNode(id="f", kind="rhetoric", label="fallacy"))
    g.add_edge(GraphEdge(source="f", target="a", kind="evaluates"))
    assert len(g.neighbors("a")) == 1