from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ALLOWED_WORKFLOW_SCOPES: Tuple[str, ...] = (
    "local_app_workflow",
    "server_workflow",
    "device_assisted_workflow",
)

ALLOWED_EXECUTION_TIERS: Tuple[str, ...] = (
    "mobile_local",
    "server_local",
    "hybrid",
    "cloud_optional",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in workflow scope contracts")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow scope contracts")


@dataclass(frozen=True)
class LocalWorkflowScopeContract:
    scope_id: str
    workflow_scope: str
    execution_tier: str
    mobile_local_first: bool
    server_optional: bool = True
    explicit_permission_required: bool = True
    user_approval_required: bool = True
    audit_visible: bool = True
    dashboard_visible: bool = True
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
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope_id", _require_non_empty_text(self.scope_id, "scope_id"))
        object.__setattr__(
            self,
            "workflow_scope",
            _require_allowed(self.workflow_scope, "workflow_scope", ALLOWED_WORKFLOW_SCOPES),
        )
        object.__setattr__(
            self,
            "execution_tier",
            _require_allowed(self.execution_tier, "execution_tier", ALLOWED_EXECUTION_TIERS),
        )

        if self.execution_tier == "mobile_local" and self.mobile_local_first is not True:
            raise ValueError("mobile_local execution tier requires mobile_local_first=True")

        _require_true(self.server_optional, "server_optional")
        _require_true(self.explicit_permission_required, "explicit_permission_required")
        _require_true(self.user_approval_required, "user_approval_required")
        _require_true(self.audit_visible, "audit_visible")
        _require_true(self.dashboard_visible, "dashboard_visible")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.execution_authority_allowed, "execution_authority_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def allowed_node_execution_tiers(self) -> Tuple[str, ...]:
        if self.execution_tier == "mobile_local":
            return ("mobile_local",)
        if self.execution_tier == "server_local":
            return ("server_local",)
        if self.execution_tier == "hybrid":
            return ALLOWED_EXECUTION_TIERS
        return ("mobile_local", "cloud_optional")

    def to_read_model(self) -> dict[str, object]:
        return {
            "scope_id": self.scope_id,
            "workflow_scope": self.workflow_scope,
            "execution_tier": self.execution_tier,
            "mobile_local_first": self.mobile_local_first,
            "server_optional": self.server_optional,
            "explicit_permission_required": self.explicit_permission_required,
            "user_approval_required": self.user_approval_required,
            "audit_visible": self.audit_visible,
            "dashboard_visible": self.dashboard_visible,
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
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_mobile_local_workflow_scope_contract(scope_id: str = "mobile_local_app_workflow") -> LocalWorkflowScopeContract:
    return LocalWorkflowScopeContract(
        scope_id=scope_id,
        workflow_scope="local_app_workflow",
        execution_tier="mobile_local",
        mobile_local_first=True,
    )


def build_default_local_workflow_scopes() -> Tuple[LocalWorkflowScopeContract, ...]:
    return (
        build_mobile_local_workflow_scope_contract("mobile_local_app_workflow"),
        LocalWorkflowScopeContract(
            scope_id="server_local_workflow",
            workflow_scope="server_workflow",
            execution_tier="server_local",
            mobile_local_first=False,
        ),
        LocalWorkflowScopeContract(
            scope_id="hybrid_workflow",
            workflow_scope="device_assisted_workflow",
            execution_tier="hybrid",
            mobile_local_first=True,
        ),
        LocalWorkflowScopeContract(
            scope_id="cloud_optional_workflow",
            workflow_scope="device_assisted_workflow",
            execution_tier="cloud_optional",
            mobile_local_first=True,
        ),
    )


__all__ = [
    "ALLOWED_EXECUTION_TIERS",
    "ALLOWED_WORKFLOW_SCOPES",
    "LocalWorkflowScopeContract",
    "build_default_local_workflow_scopes",
    "build_mobile_local_workflow_scope_contract",
]
