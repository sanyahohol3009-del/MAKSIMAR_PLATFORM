from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import MemoryComponentProjection, MEMORY_COMPONENT_INVENTORY_SCOPE


MemoryMapNodeKind = Literal[
    "memory_layer",
    "backend_adapter",
    "governance_layer",
    "dashboard_view",
    "evidence_layer",
]


@dataclass(frozen=True, slots=True)
class FinalMemoryMapNode:
    node_id: str
    label: str
    node_kind: MemoryMapNodeKind
    source_path: str
    read_only: bool
    dashboard_visible: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    node_ready: bool
    classification: str = "READ_MODEL"
    runtime_status: str = "HISTORICAL_CONTRACT_PREVIEW"
    owner: str = "historical_memory_foundation"
    storage_path: str = ""
    persistence: str = "contract metadata; not proof of a populated store"
    writer: str = ""
    write_scope: str = ""
    canonical_store_surface: str = ""
    logical_roles: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id must be non-empty")
        if not self.label:
            raise ValueError("label must be non-empty")
        if not self.source_path:
            raise ValueError("source_path must be non-empty")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.dashboard_visible is not True:
            raise ValueError("dashboard_visible must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.node_ready is not True:
            raise ValueError("node_ready must be True")


@dataclass(frozen=True, slots=True)
class FinalMemoryMapEdge:
    edge_id: str
    from_node_id: str
    to_node_id: str
    relation: str
    read_only_relation: bool
    edge_ready: bool

    def __post_init__(self) -> None:
        if not self.edge_id:
            raise ValueError("edge_id must be non-empty")
        if not self.from_node_id:
            raise ValueError("from_node_id must be non-empty")
        if not self.to_node_id:
            raise ValueError("to_node_id must be non-empty")
        if self.from_node_id == self.to_node_id:
            raise ValueError("from_node_id and to_node_id must differ")
        if not self.relation:
            raise ValueError("relation must be non-empty")
        if self.read_only_relation is not True:
            raise ValueError("read_only_relation must be True")
        if self.edge_ready is not True:
            raise ValueError("edge_ready must be True")


@dataclass(frozen=True, slots=True)
class FinalMemoryMap:
    map_id: str
    nodes: Tuple[FinalMemoryMapNode, ...]
    edges: Tuple[FinalMemoryMapEdge, ...]
    all_registered_modules_visible: bool
    all_storage_nodes_visible: bool
    all_retrieval_sources_visible: bool
    dashboard_read_only: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    map_ready: bool
    inventory_coverage: str = "REGISTERED_NATIVE_SURFACES_ONLY"
    whole_organism_inventory_complete: bool = False
    registered_surface_ids: Tuple[str, ...] = ()
    logical_components: Tuple[MemoryComponentProjection, ...] = ()
    component_inventory_scope: str = MEMORY_COMPONENT_INVENTORY_SCOPE

    def __post_init__(self) -> None:
        if not self.map_id:
            raise ValueError("map_id must be non-empty")
        if not self.nodes:
            raise ValueError("nodes must be non-empty")
        if not self.edges:
            raise ValueError("edges must be non-empty")
        component_ids = tuple(item.component_id for item in self.logical_components)
        if len(set(component_ids)) != len(component_ids):
            raise ValueError("logical component identities must be unique")
        node_ids = {node.node_id for node in self.nodes}
        if len(set(self.registered_surface_ids)) != len(self.registered_surface_ids):
            raise ValueError("registered surface identities must be unique")
        if not set(self.registered_surface_ids).issubset(node_ids):
            raise ValueError("registered surface node missing")
        if set(component_ids).intersection(self.registered_surface_ids):
            raise ValueError("component classification must not enroll a retrieval surface")
        if len(node_ids) != len(self.nodes):
            raise ValueError("node_id values must be unique")
        for edge in self.edges:
            if edge.from_node_id not in node_ids:
                raise ValueError(f"edge from_node_id missing: {edge.from_node_id}")
            if edge.to_node_id not in node_ids:
                raise ValueError(f"edge to_node_id missing: {edge.to_node_id}")
        if not self.all_registered_modules_visible:
            raise ValueError("all_registered_modules_visible must be True")
        if not self.all_storage_nodes_visible:
            raise ValueError("all_storage_nodes_visible must be True")
        if not self.all_retrieval_sources_visible:
            raise ValueError("all_retrieval_sources_visible must be True")
        if not self.dashboard_read_only:
            raise ValueError("dashboard_read_only must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.map_ready:
            raise ValueError("map_ready must be True")
