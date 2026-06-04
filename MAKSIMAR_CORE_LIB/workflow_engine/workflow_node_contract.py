from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ALLOWED_WORKFLOW_NODE_KINDS: Tuple[str, ...] = (
    "trigger",
    "action",
    "condition",
    "transform",
    "approval",
    "audit",
    "handoff",
    "status",
    "tool_intent",
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


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str) -> Tuple[str, ...]:
    if values is None:
        return ()
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized_values = tuple(_require_non_empty_text(value, field_name) for value in values)
    if len(set(normalized_values)) != len(normalized_values):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized_values


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow graph contracts")


@dataclass(frozen=True)
class WorkflowNodeContract:
    node_id: str
    node_kind: str
    display_name: str
    n8n_compatible_type: str
    execution_tier: str
    capability_refs: Tuple[str, ...] = ()
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
        object.__setattr__(self, "node_id", _require_non_empty_text(self.node_id, "node_id"))
        object.__setattr__(
            self,
            "node_kind",
            _require_allowed(self.node_kind, "node_kind", ALLOWED_WORKFLOW_NODE_KINDS),
        )
        object.__setattr__(self, "display_name", _require_non_empty_text(self.display_name, "display_name"))
        object.__setattr__(
            self,
            "n8n_compatible_type",
            _require_non_empty_text(self.n8n_compatible_type, "n8n_compatible_type"),
        )
        object.__setattr__(
            self,
            "execution_tier",
            _require_allowed(self.execution_tier, "execution_tier", ALLOWED_EXECUTION_TIERS),
        )
        object.__setattr__(
            self,
            "capability_refs",
            _normalize_text_tuple(self.capability_refs, "capability_refs"),
        )

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
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "node_kind": self.node_kind,
            "display_name": self.display_name,
            "n8n_compatible_type": self.n8n_compatible_type,
            "execution_tier": self.execution_tier,
            "capability_refs": self.capability_refs,
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


def build_workflow_node_contract(
    *,
    node_id: str,
    node_kind: str,
    display_name: str,
    n8n_compatible_type: str,
    execution_tier: str = "mobile_local",
    capability_refs: Tuple[str, ...] = (),
) -> WorkflowNodeContract:
    return WorkflowNodeContract(
        node_id=node_id,
        node_kind=node_kind,
        display_name=display_name,
        n8n_compatible_type=n8n_compatible_type,
        execution_tier=execution_tier,
        capability_refs=capability_refs,
    )


__all__ = [
    "ALLOWED_EXECUTION_TIERS",
    "ALLOWED_WORKFLOW_NODE_KINDS",
    "WorkflowNodeContract",
    "build_workflow_node_contract",
]
