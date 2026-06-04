from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import (
    WorkflowGraphContract,
    build_sample_workflow_graph_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    WorkflowSafetyPolicyContract,
    build_workflow_safety_policy_contract,
)


WORKFLOW_AUTOMATION_CONTAINER_CONTRACT_PATH = (
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml"
)
WORKFLOW_AUTOMATION_RUNTIME_PROFILE_PATH = (
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml"
)
WORKFLOW_AUTOMATION_NETWORK_POLICY_PATH = (
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml"
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str, *, require_non_empty: bool) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in workflow status bridge")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow status bridge")


@dataclass(frozen=True)
class WorkflowStatusBridgeReadModel:
    bridge_id: str
    graph_id: str
    graph_schema_version: str
    node_count: int
    edge_count: int
    execution_tier: str
    status_panel_id: str
    preview_tool_path: str
    container_contract_path: str
    runtime_profile_path: str
    network_policy_path: str
    visible_status_items: Tuple[str, ...]
    readiness_flags: Tuple[str, ...]
    dashboard_read_only: bool = True
    preview_read_only: bool = True
    status_bridge_only: bool = True
    container_contract_declared: bool = True
    runtime_profile_declared: bool = True
    network_policy_declared: bool = True
    network_disabled_by_default: bool = True
    socket_disabled_by_default: bool = True
    tunnel_disabled_by_default: bool = True
    runtime_execution_allowed: bool = False
    dashboard_execution_allowed: bool = False
    preview_execution_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_phone_control_allowed: bool = False
    runtime_mutation_allowed: bool = False
    n8n_download_allowed_now: bool = False
    n8n_install_allowed_now: bool = False
    n8n_production_runtime_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _require_non_empty_text(self.bridge_id, "bridge_id"))
        object.__setattr__(self, "graph_id", _require_non_empty_text(self.graph_id, "graph_id"))
        object.__setattr__(
            self,
            "graph_schema_version",
            _require_non_empty_text(self.graph_schema_version, "graph_schema_version"),
        )
        if not isinstance(self.node_count, int) or self.node_count < 1:
            raise ValueError("node_count must be a positive integer")
        if not isinstance(self.edge_count, int) or self.edge_count < 0:
            raise ValueError("edge_count must be a non-negative integer")
        object.__setattr__(self, "execution_tier", _require_non_empty_text(self.execution_tier, "execution_tier"))
        object.__setattr__(self, "status_panel_id", _require_non_empty_text(self.status_panel_id, "status_panel_id"))
        object.__setattr__(self, "preview_tool_path", _require_non_empty_text(self.preview_tool_path, "preview_tool_path"))
        object.__setattr__(
            self,
            "container_contract_path",
            _require_non_empty_text(self.container_contract_path, "container_contract_path"),
        )
        object.__setattr__(
            self,
            "runtime_profile_path",
            _require_non_empty_text(self.runtime_profile_path, "runtime_profile_path"),
        )
        object.__setattr__(
            self,
            "network_policy_path",
            _require_non_empty_text(self.network_policy_path, "network_policy_path"),
        )
        object.__setattr__(
            self,
            "visible_status_items",
            _normalize_text_tuple(self.visible_status_items, "visible_status_items", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "readiness_flags",
            _normalize_text_tuple(self.readiness_flags, "readiness_flags", require_non_empty=True),
        )

        _require_true(self.dashboard_read_only, "dashboard_read_only")
        _require_true(self.preview_read_only, "preview_read_only")
        _require_true(self.status_bridge_only, "status_bridge_only")
        _require_true(self.container_contract_declared, "container_contract_declared")
        _require_true(self.runtime_profile_declared, "runtime_profile_declared")
        _require_true(self.network_policy_declared, "network_policy_declared")
        _require_true(self.network_disabled_by_default, "network_disabled_by_default")
        _require_true(self.socket_disabled_by_default, "socket_disabled_by_default")
        _require_true(self.tunnel_disabled_by_default, "tunnel_disabled_by_default")

        _require_false(self.runtime_execution_allowed, "runtime_execution_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.preview_execution_allowed, "preview_execution_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.n8n_download_allowed_now, "n8n_download_allowed_now")
        _require_false(self.n8n_install_allowed_now, "n8n_install_allowed_now")
        _require_false(self.n8n_production_runtime_allowed, "n8n_production_runtime_allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "bridge_id": self.bridge_id,
            "graph_id": self.graph_id,
            "graph_schema_version": self.graph_schema_version,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "execution_tier": self.execution_tier,
            "status_panel_id": self.status_panel_id,
            "preview_tool_path": self.preview_tool_path,
            "container_contract_path": self.container_contract_path,
            "runtime_profile_path": self.runtime_profile_path,
            "network_policy_path": self.network_policy_path,
            "visible_status_items": self.visible_status_items,
            "readiness_flags": self.readiness_flags,
            "dashboard_read_only": self.dashboard_read_only,
            "preview_read_only": self.preview_read_only,
            "status_bridge_only": self.status_bridge_only,
            "container_contract_declared": self.container_contract_declared,
            "runtime_profile_declared": self.runtime_profile_declared,
            "network_policy_declared": self.network_policy_declared,
            "network_disabled_by_default": self.network_disabled_by_default,
            "socket_disabled_by_default": self.socket_disabled_by_default,
            "tunnel_disabled_by_default": self.tunnel_disabled_by_default,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "preview_execution_allowed": self.preview_execution_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "n8n_download_allowed_now": self.n8n_download_allowed_now,
            "n8n_install_allowed_now": self.n8n_install_allowed_now,
            "n8n_production_runtime_allowed": self.n8n_production_runtime_allowed,
        }


def build_workflow_status_bridge_read_model(
    *,
    graph: WorkflowGraphContract | None = None,
    safety_policy: WorkflowSafetyPolicyContract | None = None,
) -> WorkflowStatusBridgeReadModel:
    active_graph = graph or build_sample_workflow_graph_contract()
    active_policy = safety_policy or build_workflow_safety_policy_contract()

    if not isinstance(active_graph, WorkflowGraphContract):
        raise TypeError("graph must be a WorkflowGraphContract")
    if not isinstance(active_policy, WorkflowSafetyPolicyContract):
        raise TypeError("safety_policy must be a WorkflowSafetyPolicyContract")
    if active_policy.dashboard_execution_allowed is not False:
        raise ValueError("workflow status bridge requires dashboard_execution_allowed=False")

    return WorkflowStatusBridgeReadModel(
        bridge_id="phase6.workflow.status.bridge.v1",
        graph_id=active_graph.graph_id,
        graph_schema_version=active_graph.schema_version,
        node_count=len(active_graph.nodes),
        edge_count=len(active_graph.edges),
        execution_tier=active_graph.local_scope.execution_tier,
        status_panel_id="workflow_automation.status.read_only",
        preview_tool_path="tools/workflow_status_preview.py",
        container_contract_path=WORKFLOW_AUTOMATION_CONTAINER_CONTRACT_PATH,
        runtime_profile_path=WORKFLOW_AUTOMATION_RUNTIME_PROFILE_PATH,
        network_policy_path=WORKFLOW_AUTOMATION_NETWORK_POLICY_PATH,
        visible_status_items=(
            "graph_contract",
            "governance_contracts",
            "server_adapter_boundary",
            "mobile_local_boundary",
            "dashboard_read_only",
            "container_contract",
            "network_policy",
        ),
        readiness_flags=(
            "workflow_graph_contract_ready",
            "workflow_governance_contracts_ready",
            "server_n8n_adapter_boundary_ready",
            "mobile_local_workflow_boundary_ready",
            "dashboard_preview_read_only",
            "container_contract_declared",
            "network_disabled_by_default",
        ),
    )


def build_workflow_dashboard_read_only_projection() -> dict[str, object]:
    read_model = build_workflow_status_bridge_read_model()
    return {
        "panel_id": read_model.status_panel_id,
        "panel_kind": "read_only_status",
        "source_bridge": read_model.bridge_id,
        "payload": read_model.to_read_model(),
        "action_controls_enabled": False,
        "execution_controls_enabled": False,
        "mutation_controls_enabled": False,
    }


__all__ = [
    "WORKFLOW_AUTOMATION_CONTAINER_CONTRACT_PATH",
    "WORKFLOW_AUTOMATION_NETWORK_POLICY_PATH",
    "WORKFLOW_AUTOMATION_RUNTIME_PROFILE_PATH",
    "WorkflowStatusBridgeReadModel",
    "build_workflow_dashboard_read_only_projection",
    "build_workflow_status_bridge_read_model",
]
