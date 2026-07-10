from hanani.ontology import (
    COHERENCE_GRAPH_EDGES,
    COHERENCE_LEVELS,
    HISTORICAL_ANCHORS,
    LAYERS,
    ONTOLOGY_VERSION,
    PARTY_TYPES,
    list_layers,
)


def test_ontology_version_is_semver_like() -> None:
    assert ONTOLOGY_VERSION == "0.3"


def test_coherence_constants() -> None:
    assert "fragmented" in COHERENCE_LEVELS
    assert "collective_alliance" in PARTY_TYPES
    assert "lcd_binding_member" in COHERENCE_GRAPH_EDGES


def test_all_five_layers_present() -> None:
    assert len(LAYERS) == 5
    assert sum(len(v) for v in LAYERS.values()) >= 30


def test_historical_anchors_seeded() -> None:
    assert "cuban_missile_crisis_1962" in HISTORICAL_ANCHORS
    assert "russia_ukraine_2014_2022_plus" in HISTORICAL_ANCHORS


def test_list_layers_returns_copy() -> None:
    layers = list_layers()
    layers["L1_superstructure"].append("bogus")
    assert "bogus" not in LAYERS["L1_superstructure"]