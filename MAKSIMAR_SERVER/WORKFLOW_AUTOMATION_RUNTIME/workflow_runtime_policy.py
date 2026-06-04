from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import N8nAdapterContract


ALLOWED_RUNTIME_POLICY_MODES: Tuple[str, ...] = (
    "contract_only",
    "intent_metadata_only",
    "sandbox_probe_prepared",
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
        raise ValueError(f"{field_name} must be True in server workflow runtime policy")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in server workflow runtime policy")


@dataclass(frozen=True)
class WorkflowRuntimePolicy:
    policy_id: str
    runtime_mode: str
    allowed_adapter_ids: Tuple[str, ...]
    allowed_execution_tiers: Tuple[str, ...]
    server_optional_accelerator: bool = True
    intent_metadata_only: bool = True
    requires_workflow_safety_policy: bool = True
    requires_permission_decision: bool = True
    requires_approval_ticket: bool = True
    requires_audit_event: bool = True
    requires_vendor_gate_for_n8n: bool = True
    requires_sandbox_boundary_for_n8n: bool = True
    requires_container_boundary_for_n8n: bool = True
    contract_only: bool = True
    runtime_execution_allowed_now: bool = False
    n8n_download_allowed_now: bool = False
    n8n_install_allowed_now: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_phone_control_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    runtime_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", _require_non_empty_text(self.policy_id, "policy_id"))
        object.__setattr__(
            self,
            "runtime_mode",
            _require_allowed(self.runtime_mode, "runtime_mode", ALLOWED_RUNTIME_POLICY_MODES),
        )
        object.__setattr__(
            self,
            "allowed_adapter_ids",
            _normalize_text_tuple(self.allowed_adapter_ids, "allowed_adapter_ids", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "allowed_execution_tiers",
            _normalize_text_tuple(
                self.allowed_execution_tiers,
                "allowed_execution_tiers",
                require_non_empty=True,
            ),
        )

        _require_true(self.server_optional_accelerator, "server_optional_accelerator")
        _require_true(self.intent_metadata_only, "intent_metadata_only")
        _require_true(self.requires_workflow_safety_policy, "requires_workflow_safety_policy")
        _require_true(self.requires_permission_decision, "requires_permission_decision")
        _require_true(self.requires_approval_ticket, "requires_approval_ticket")
        _require_true(self.requires_audit_event, "requires_audit_event")
        _require_true(self.requires_vendor_gate_for_n8n, "requires_vendor_gate_for_n8n")
        _require_true(self.requires_sandbox_boundary_for_n8n, "requires_sandbox_boundary_for_n8n")
        _require_true(self.requires_container_boundary_for_n8n, "requires_container_boundary_for_n8n")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.runtime_execution_allowed_now, "runtime_execution_allowed_now")
        _require_false(self.n8n_download_allowed_now, "n8n_download_allowed_now")
        _require_false(self.n8n_install_allowed_now, "n8n_install_allowed_now")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")

    def allows_adapter_contract(self, adapter: N8nAdapterContract) -> bool:
        if not isinstance(adapter, N8nAdapterContract):
            raise TypeError("adapter must be an N8nAdapterContract")
        return (
            adapter.adapter_id in self.allowed_adapter_ids
            and adapter.external_adapter_only is True
            and adapter.n8n_is_core is False
            and adapter.download_allowed_now is False
            and adapter.install_allowed_now is False
            and adapter.runtime_execution_allowed_now is False
        )

    def allows_execution_tier(self, execution_tier: str) -> bool:
        normalized = _require_non_empty_text(execution_tier, "execution_tier")
        return normalized in self.allowed_execution_tiers

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "runtime_mode": self.runtime_mode,
            "allowed_adapter_ids": self.allowed_adapter_ids,
            "allowed_execution_tiers": self.allowed_execution_tiers,
            "server_optional_accelerator": self.server_optional_accelerator,
            "intent_metadata_only": self.intent_metadata_only,
            "requires_workflow_safety_policy": self.requires_workflow_safety_policy,
            "requires_permission_decision": self.requires_permission_decision,
            "requires_approval_ticket": self.requires_approval_ticket,
            "requires_audit_event": self.requires_audit_event,
            "requires_vendor_gate_for_n8n": self.requires_vendor_gate_for_n8n,
            "requires_sandbox_boundary_for_n8n": self.requires_sandbox_boundary_for_n8n,
            "requires_container_boundary_for_n8n": self.requires_container_boundary_for_n8n,
            "contract_only": self.contract_only,
            "runtime_execution_allowed_now": self.runtime_execution_allowed_now,
            "n8n_download_allowed_now": self.n8n_download_allowed_now,
            "n8n_install_allowed_now": self.n8n_install_allowed_now,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }


def build_workflow_runtime_policy(adapter: N8nAdapterContract | None = None) -> WorkflowRuntimePolicy:
    adapter_id = adapter.adapter_id if adapter is not None else "phase6.n8n.external.adapter.v1"
    return WorkflowRuntimePolicy(
        policy_id="phase6.server.workflow.runtime.policy.v1",
        runtime_mode="intent_metadata_only",
        allowed_adapter_ids=(adapter_id,),
        allowed_execution_tiers=("mobile_local", "server_local", "hybrid", "cloud_optional"),
    )


__all__ = [
    "ALLOWED_RUNTIME_POLICY_MODES",
    "WorkflowRuntimePolicy",
    "build_workflow_runtime_policy",
]
