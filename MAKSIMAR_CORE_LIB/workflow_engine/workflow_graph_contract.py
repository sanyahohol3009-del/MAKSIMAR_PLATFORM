from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.local_workflow_scope_contract import (
    LocalWorkflowScopeContract,
    build_mobile_local_workflow_scope_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_edge_contract import WorkflowEdgeContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_node_contract import WorkflowNodeContract


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_nodes(nodes: Tuple[WorkflowNodeContract, ...]) -> Tuple[WorkflowNodeContract, ...]:
    if not isinstance(nodes, tuple):
        raise TypeError("nodes must be a tuple of WorkflowNodeContract objects")
    if not nodes:
        raise ValueError("workflow graph must contain at least one node")
    for node in nodes:
        if not isinstance(node, WorkflowNodeContract):
            raise TypeError("nodes must contain only WorkflowNodeContract objects")
    node_ids = tuple(node.node_id for node in nodes)
    if len(set(node_ids)) != len(node_ids):
        raise ValueError("workflow graph node ids must be unique")
    return nodes


def _normalize_edges(edges: Tuple[WorkflowEdgeContract, ...]) -> Tuple[WorkflowEdgeContract, ...]:
    if not isinstance(edges, tuple):
        raise TypeError("edges must be a tuple of WorkflowEdgeContract objects")
    for edge in edges:
        if not isinstance(edge, WorkflowEdgeContract):
            raise TypeError("edges must contain only WorkflowEdgeContract objects")
    edge_ids = tuple(edge.edge_id for edge in edges)
    if len(set(edge_ids)) != len(edge_ids):
        raise ValueError("workflow graph edge ids must be unique")
    return edges


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow graph contracts")


@dataclass(frozen=True)
class WorkflowGraphContract:
    graph_id: str
    schema_version: str
    display_name: str
    nodes: Tuple[WorkflowNodeContract, ...]
    edges: Tuple[WorkflowEdgeContract, ...]
    local_scope: LocalWorkflowScopeContract
    n8n_compatible: bool = True
    contract_only: bool = True
    execution_authority_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    runtime_mutation_allowed: bool = False
    graph_defines_workflow_truth: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "graph_id", _require_non_empty_text(self.graph_id, "graph_id"))
        object.__setattr__(self, "schema_version", _require_non_empty_text(self.schema_version, "schema_version"))
        object.__setattr__(self, "display_name", _require_non_empty_text(self.display_name, "display_name"))
        object.__setattr__(self, "nodes", _normalize_nodes(self.nodes))
        object.__setattr__(self, "edges", _normalize_edges(self.edges))

        if not isinstance(self.local_scope, LocalWorkflowScopeContract):
            raise TypeError("local_scope must be a LocalWorkflowScopeContract")
        if self.n8n_compatible is not True:
            raise ValueError("n8n_compatible must be True for PHASE 6 graph contracts")
        if self.contract_only is not True:
            raise ValueError("contract_only must be True in workflow graph contracts")

        _require_false(self.execution_authority_allowed, "execution_authority_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.graph_defines_workflow_truth, "graph_defines_workflow_truth")

        self._validate_edges_reference_existing_nodes()
        self._validate_node_tiers_match_scope()

    def _validate_edges_reference_existing_nodes(self) -> None:
        node_ids = {node.node_id for node in self.nodes}
        for edge in self.edges:
            source_id, target_id = edge.referenced_node_ids()
            if source_id not in node_ids:
                raise ValueError(f"edge {edge.edge_id} references missing source node {source_id}")
            if target_id not in node_ids:
                raise ValueError(f"edge {edge.edge_id} references missing target node {target_id}")

    def _validate_node_tiers_match_scope(self) -> None:
        allowed_tiers = set(self.local_scope.allowed_node_execution_tiers())
        for node in self.nodes:
            if node.execution_tier not in allowed_tiers:
                raise ValueError(
                    f"node {node.node_id} execution_tier={node.execution_tier} is not allowed "
                    f"for scope execution_tier={self.local_scope.execution_tier}"
                )

    def node_ids(self) -> Tuple[str, ...]:
        return tuple(node.node_id for node in self.nodes)

    def edge_ids(self) -> Tuple[str, ...]:
        return tuple(edge.edge_id for edge in self.edges)

    def to_read_model(self) -> dict[str, object]:
        return {
            "graph_id": self.graph_id,
            "schema_version": self.schema_version,
            "display_name": self.display_name,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "node_ids": self.node_ids(),
            "edge_ids": self.edge_ids(),
            "local_scope": self.local_scope.to_read_model(),
            "n8n_compatible": self.n8n_compatible,
            "contract_only": self.contract_only,
            "execution_authority_allowed": self.execution_authority_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "graph_defines_workflow_truth": self.graph_defines_workflow_truth,
        }


def build_sample_workflow_graph_contract() -> WorkflowGraphContract:
    nodes = (
        WorkflowNodeContract(
            node_id="trigger.manual",
            node_kind="trigger",
            display_name="Manual Local Trigger",
            n8n_compatible_type="n8n.manualTrigger",
            execution_tier="mobile_local",
            capability_refs=("local_app_workflow",),
        ),
        WorkflowNodeContract(
            node_id="proposal.local_ai",
            node_kind="tool_intent",
            display_name="Local AI Workflow Proposal",
            n8n_compatible_type="maksimar.localAiWorkflowProposal",
            execution_tier="mobile_local",
            capability_refs=("local_ai_workflow_proposal",),
        ),
        WorkflowNodeContract(
            node_id="approval.user",
            node_kind="approval",
            display_name="User Approval Gate",
            n8n_compatible_type="maksimar.userApprovalGate",
            execution_tier="mobile_local",
            capability_refs=("explicit_user_approval",),
        ),
    )
    edges = (
        WorkflowEdgeContract(
            edge_id="edge.trigger.to.proposal",
            source_node_id="trigger.manual",
            target_node_id="proposal.local_ai",
            edge_kind="main",
            n8n_connection_type="main",
        ),
        WorkflowEdgeContract(
            edge_id="edge.proposal.to.approval",
            source_node_id="proposal.local_ai",
            target_node_id="approval.user",
            edge_kind="approval",
            n8n_connection_type="approval",
        ),
    )
    return WorkflowGraphContract(
        graph_id="sample.mobile_local.workflow",
        schema_version="phase6.graph.v1",
        display_name="Sample Mobile Local Workflow",
        nodes=nodes,
        edges=edges,
        local_scope=build_mobile_local_workflow_scope_contract(),
    )


def validate_workflow_graph_contract(graph: WorkflowGraphContract) -> bool:
    if not isinstance(graph, WorkflowGraphContract):
        raise TypeError("graph must be a WorkflowGraphContract")
    WorkflowGraphContract(
        graph_id=graph.graph_id,
        schema_version=graph.schema_version,
        display_name=graph.display_name,
        nodes=graph.nodes,
        edges=graph.edges,
        local_scope=graph.local_scope,
        n8n_compatible=graph.n8n_compatible,
        contract_only=graph.contract_only,
        execution_authority_allowed=graph.execution_authority_allowed,
        direct_core_write_allowed=graph.direct_core_write_allowed,
        direct_server_canonical_write_allowed=graph.direct_server_canonical_write_allowed,
        network_allowed=graph.network_allowed,
        socket_allowed=graph.socket_allowed,
        tunnel_allowed=graph.tunnel_allowed,
        network_socket_tunnel_allowed=graph.network_socket_tunnel_allowed,
        hidden_remote_control_allowed=graph.hidden_remote_control_allowed,
        runtime_mutation_allowed=graph.runtime_mutation_allowed,
        graph_defines_workflow_truth=graph.graph_defines_workflow_truth,
    )
    return True


__all__ = [
    "WorkflowGraphContract",
    "build_sample_workflow_graph_contract",
    "validate_workflow_graph_contract",
]
