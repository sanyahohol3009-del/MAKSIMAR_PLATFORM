from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.local_workflow_scope_contract import ALLOWED_EXECUTION_TIERS
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_edge_contract import ALLOWED_WORKFLOW_EDGE_KINDS
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import WorkflowGraphContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_node_contract import ALLOWED_WORKFLOW_NODE_KINDS


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_supported_values(
    values: Tuple[str, ...],
    field_name: str,
    allowed_values: Tuple[str, ...],
) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    if not values:
        raise ValueError(f"{field_name} must not be empty")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    unknown_values = tuple(value for value in normalized if value not in allowed_values)
    if unknown_values:
        raise ValueError(f"{field_name} contains unsupported values: {unknown_values}")
    return normalized


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in n8n compatibility contracts")


@dataclass(frozen=True)
class N8nGraphCompatibilityContract:
    compatibility_id: str = "phase6.n8n.graph.compatibility.v1"
    adapter_boundary: str = "external_server_adapter_container_runtime"
    supported_node_kinds: Tuple[str, ...] = field(default_factory=lambda: ALLOWED_WORKFLOW_NODE_KINDS)
    supported_edge_kinds: Tuple[str, ...] = field(default_factory=lambda: ALLOWED_WORKFLOW_EDGE_KINDS)
    supported_execution_tiers: Tuple[str, ...] = field(default_factory=lambda: ALLOWED_EXECUTION_TIERS)
    n8n_is_core: bool = False
    mobile_embeds_n8n: bool = False
    n8n_defines_workflow_truth: bool = False
    execution_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    runtime_mutation_allowed: bool = False
    contract_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "compatibility_id",
            _require_non_empty_text(self.compatibility_id, "compatibility_id"),
        )
        object.__setattr__(
            self,
            "adapter_boundary",
            _require_non_empty_text(self.adapter_boundary, "adapter_boundary"),
        )
        object.__setattr__(
            self,
            "supported_node_kinds",
            _normalize_supported_values(
                self.supported_node_kinds,
                "supported_node_kinds",
                ALLOWED_WORKFLOW_NODE_KINDS,
            ),
        )
        object.__setattr__(
            self,
            "supported_edge_kinds",
            _normalize_supported_values(
                self.supported_edge_kinds,
                "supported_edge_kinds",
                ALLOWED_WORKFLOW_EDGE_KINDS,
            ),
        )
        object.__setattr__(
            self,
            "supported_execution_tiers",
            _normalize_supported_values(
                self.supported_execution_tiers,
                "supported_execution_tiers",
                ALLOWED_EXECUTION_TIERS,
            ),
        )

        if self.contract_only is not True:
            raise ValueError("contract_only must be True in n8n compatibility contracts")

        _require_false(self.n8n_is_core, "n8n_is_core")
        _require_false(self.mobile_embeds_n8n, "mobile_embeds_n8n")
        _require_false(self.n8n_defines_workflow_truth, "n8n_defines_workflow_truth")
        _require_false(self.execution_allowed, "execution_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "compatibility_id": self.compatibility_id,
            "adapter_boundary": self.adapter_boundary,
            "supported_node_kinds": self.supported_node_kinds,
            "supported_edge_kinds": self.supported_edge_kinds,
            "supported_execution_tiers": self.supported_execution_tiers,
            "n8n_is_core": self.n8n_is_core,
            "mobile_embeds_n8n": self.mobile_embeds_n8n,
            "n8n_defines_workflow_truth": self.n8n_defines_workflow_truth,
            "execution_allowed": self.execution_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "contract_only": self.contract_only,
        }


def build_n8n_graph_compatibility_contract() -> N8nGraphCompatibilityContract:
    return N8nGraphCompatibilityContract()


def validate_n8n_compatible_graph(
    graph: WorkflowGraphContract,
    compatibility: N8nGraphCompatibilityContract | None = None,
) -> bool:
    if not isinstance(graph, WorkflowGraphContract):
        raise TypeError("graph must be a WorkflowGraphContract")
    active_compatibility = compatibility or build_n8n_graph_compatibility_contract()

    if graph.n8n_compatible is not True:
        raise ValueError("workflow graph must be marked n8n_compatible=True")

    supported_node_kinds = set(active_compatibility.supported_node_kinds)
    supported_edge_kinds = set(active_compatibility.supported_edge_kinds)
    supported_execution_tiers = set(active_compatibility.supported_execution_tiers)

    for node in graph.nodes:
        if node.node_kind not in supported_node_kinds:
            raise ValueError(f"node {node.node_id} has unsupported node_kind={node.node_kind}")
        if node.execution_tier not in supported_execution_tiers:
            raise ValueError(f"node {node.node_id} has unsupported execution_tier={node.execution_tier}")
        if not node.n8n_compatible_type:
            raise ValueError(f"node {node.node_id} must define n8n_compatible_type")

    for edge in graph.edges:
        if edge.edge_kind not in supported_edge_kinds:
            raise ValueError(f"edge {edge.edge_id} has unsupported edge_kind={edge.edge_kind}")
        if not edge.n8n_connection_type:
            raise ValueError(f"edge {edge.edge_id} must define n8n_connection_type")

    return True


__all__ = [
    "N8nGraphCompatibilityContract",
    "build_n8n_graph_compatibility_contract",
    "validate_n8n_compatible_graph",
]
