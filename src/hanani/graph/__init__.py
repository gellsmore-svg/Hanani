"""Unified semantic graph store — mechanism + rhetoric + atoms + sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

NodeKind = Literal[
    "mechanism",
    "rhetoric",
    "logic_atom",
    "source",
    "factor",
    "historical_anchor",
    "outcome_scenario",
]

MECHANISM_EDGE_TYPES: tuple[str, ...] = (
    "part_of",
    "instance_of",
    "implies",
    "enables",
    "contradicts",
    "correlates_with",
    "exemplified_by",
    "observed_via",
    "tags",
)

RHETORIC_EDGE_TYPES: tuple[str, ...] = (
    "subtype_of",
    "violates",
    "exhibits",
    "missing_warrant",
    "supports_chain",
    "undermines",
    "detected_in",
    "contradicts",
)

ATOM_EDGE_TYPES: tuple[str, ...] = (
    "agrees",
    "contradicts",
    "complements",
    "implies",
    "gap",
    "supports",
    "weakens",
    "yields",
    "evaluates",
)


@dataclass
class GraphNode:
    id: str
    kind: NodeKind
    label: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    target: str
    kind: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticGraph:
    """In-memory graph; persistence layer comes later."""

    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def neighbors(self, node_id: str, *, kind: str | None = None) -> list[GraphEdge]:
        out = [e for e in self.edges if e.source == node_id or e.target == node_id]
        if kind:
            out = [e for e in out if e.kind == kind]
        return out

    def nodes_by_kind(self, kind: NodeKind) -> list[GraphNode]:
        return [n for n in self.nodes.values() if n.kind == kind]


def seed_mechanism_nodes(layer_registry: dict[str, list[str]]) -> SemanticGraph:
    """Bootstrap mechanism concepts from hanani.ontology.LAYERS."""
    graph = SemanticGraph()
    for layer, concepts in layer_registry.items():
        graph.add_node(GraphNode(id=layer, kind="mechanism", label=layer, properties={"tier": "layer"}))
        for concept in concepts:
            cid = f"{layer}.{concept}"
            graph.add_node(GraphNode(id=cid, kind="mechanism", label=concept))
            graph.add_edge(GraphEdge(source=cid, target=layer, kind="part_of"))
    return graph


def seed_rhetoric_nodes(fallacies: dict[str, str], enthymemes: dict[str, str]) -> SemanticGraph:
    graph = SemanticGraph()
    for fid, desc in fallacies.items():
        graph.add_node(GraphNode(id=fid, kind="rhetoric", label=fid, properties={"description": desc}))
    for eid, desc in enthymemes.items():
        graph.add_node(GraphNode(id=eid, kind="rhetoric", label=eid, properties={"description": desc, "enthymeme": True}))
    return graph


__all__ = [
    "ATOM_EDGE_TYPES",
    "GraphEdge",
    "GraphNode",
    "MECHANISM_EDGE_TYPES",
    "NodeKind",
    "RHETORIC_EDGE_TYPES",
    "SemanticGraph",
    "seed_mechanism_nodes",
    "seed_rhetoric_nodes",
]