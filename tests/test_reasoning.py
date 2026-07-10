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


def test_semantic_graph_neighbors() -> None:
    g = SemanticGraph()
    from hanani.graph import GraphEdge, GraphNode

    g.add_node(GraphNode(id="a", kind="logic_atom", label="atom"))
    g.add_node(GraphNode(id="f", kind="rhetoric", label="fallacy"))
    g.add_edge(GraphEdge(source="f", target="a", kind="evaluates"))
    assert len(g.neighbors("a")) == 1