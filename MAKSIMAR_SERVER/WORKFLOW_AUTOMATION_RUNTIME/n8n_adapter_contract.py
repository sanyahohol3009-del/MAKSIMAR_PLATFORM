from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ALLOWED_N8N_ADAPTER_MODES: Tuple[str, ...] = (
    "contract_only",
    "container_blueprint",
    "sandbox_probe_ready",
)
ALLOWED_N8N_ADAPTER_LOCATIONS: Tuple[str, ...] = (
    "external_server_adapter",
    "container_runtime",
    "sandbox_quarantine",
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
        raise ValueError(f"{field_name} must be True for the n8n adapter boundary")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False for the n8n adapter boundary")


@dataclass(frozen=True)
class N8nAdapterContract:
    adapter_id: str
    adapter_mode: str
    adapter_location: str
    supported_graph_semantics: Tuple[str, ...]
    supported_runtime_events: Tuple[str, ...]
    requires_vendor_gate: bool = True
    requires_sandbox_boundary: bool = True
    requires_container_boundary: bool = True
    requires_operator_approval: bool = True
    external_adapter_only: bool = True
    contract_only: bool = True
    n8n_is_core: bool = False
    n8n_is_canonical_truth: bool = False
    n8n_defines_workflow_truth: bool = False
    download_allowed_now: bool = False
    install_allowed_now: bool = False
    runtime_execution_allowed_now: bool = False
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
        object.__setattr__(self, "adapter_id", _require_non_empty_text(self.adapter_id, "adapter_id"))
        object.__setattr__(
            self,
            "adapter_mode",
            _require_allowed(self.adapter_mode, "adapter_mode", ALLOWED_N8N_ADAPTER_MODES),
        )
        object.__setattr__(
            self,
            "adapter_location",
            _require_allowed(self.adapter_location, "adapter_location", ALLOWED_N8N_ADAPTER_LOCATIONS),
        )
        object.__setattr__(
            self,
            "supported_graph_semantics",
            _normalize_text_tuple(
                self.supported_graph_semantics,
                "supported_graph_semantics",
                require_non_empty=True,
            ),
        )
        object.__setattr__(
            self,
            "supported_runtime_events",
            _normalize_text_tuple(
                self.supported_runtime_events,
                "supported_runtime_events",
                require_non_empty=True,
            ),
        )

        _require_true(self.requires_vendor_gate, "requires_vendor_gate")
        _require_true(self.requires_sandbox_boundary, "requires_sandbox_boundary")
        _require_true(self.requires_container_boundary, "requires_container_boundary")
        _require_true(self.requires_operator_approval, "requires_operator_approval")
        _require_true(self.external_adapter_only, "external_adapter_only")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.n8n_is_core, "n8n_is_core")
        _require_false(self.n8n_is_canonical_truth, "n8n_is_canonical_truth")
        _require_false(self.n8n_defines_workflow_truth, "n8n_defines_workflow_truth")
        _require_false(self.download_allowed_now, "download_allowed_now")
        _require_false(self.install_allowed_now, "install_allowed_now")
        _require_false(self.runtime_execution_allowed_now, "runtime_execution_allowed_now")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "adapter_mode": self.adapter_mode,
            "adapter_location": self.adapter_location,
            "supported_graph_semantics": self.supported_graph_semantics,
            "supported_runtime_events": self.supported_runtime_events,
            "requires_vendor_gate": self.requires_vendor_gate,
            "requires_sandbox_boundary": self.requires_sandbox_boundary,
            "requires_container_boundary": self.requires_container_boundary,
            "requires_operator_approval": self.requires_operator_approval,
            "external_adapter_only": self.external_adapter_only,
            "contract_only": self.contract_only,
            "n8n_is_core": self.n8n_is_core,
            "n8n_is_canonical_truth": self.n8n_is_canonical_truth,
            "n8n_defines_workflow_truth": self.n8n_defines_workflow_truth,
            "download_allowed_now": self.download_allowed_now,
            "install_allowed_now": self.install_allowed_now,
            "runtime_execution_allowed_now": self.runtime_execution_allowed_now,
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


def build_n8n_adapter_contract() -> N8nAdapterContract:
    return N8nAdapterContract(
        adapter_id="phase6.n8n.external.adapter.v1",
        adapter_mode="contract_only",
        adapter_location="external_server_adapter",
        supported_graph_semantics=(
            "nodes",
            "edges",
            "triggers",
            "actions",
            "conditions",
            "approval_gates",
            "audit_events",
            "status_projection",
        ),
        supported_runtime_events=(
            "workflow_registered",
            "intent_requested",
            "sandbox_probe_requested",
            "approval_required",
            "audit_recorded",
        ),
    )


__all__ = [
    "ALLOWED_N8N_ADAPTER_LOCATIONS",
    "ALLOWED_N8N_ADAPTER_MODES",
    "N8nAdapterContract",
    "build_n8n_adapter_contract",
]
