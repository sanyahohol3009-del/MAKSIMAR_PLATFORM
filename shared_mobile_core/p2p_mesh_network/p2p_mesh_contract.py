from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.network_backend_adapter_contract import (
    NetworkBackendAdapterContract,
    build_default_network_backend_adapter_registry,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnPolicyDisableContract,
    build_default_vpn_policy_disable_contract,
)


def _to_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        result = value.to_dict()
        if isinstance(result, dict):
            return result
    data = getattr(value, "__dict__", None)
    if isinstance(data, dict):
        return dict(data)
    return {"repr": repr(value)}


@dataclass(frozen=True, slots=True)
class P2PMeshContract:
    """Read-only shared-mobile P2P mesh contract.

    This binds to the canonical net_p2p_mesh_adapter and disable policy.
    It does not start networking.
    """

    schema_version: str
    mesh_id: str
    owner_surface: str
    p2p_adapter: NetworkBackendAdapterContract
    disable_policy: VpnPolicyDisableContract
    p2p_mesh_disabled: bool
    real_p2p_networking_allowed: bool
    peer_discovery_allowed: bool
    socket_open_allowed: bool
    ports_opened: bool
    external_network_access_enabled: bool
    tunnel_creation_allowed: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    source_of_truth_override_allowed: bool
    direct_core_authority_allowed: bool
    dashboard_visible: bool
    read_only: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "p2p_mesh_contract.v1":
            raise ValueError("schema_version must be p2p_mesh_contract.v1")
        if self.mesh_id != "shared_mobile_p2p_mesh_disabled_default":
            raise ValueError("mesh_id must be shared_mobile_p2p_mesh_disabled_default")
        if self.owner_surface != "shared_mobile_core/p2p_mesh_network":
            raise ValueError("owner_surface must be shared_mobile_core/p2p_mesh_network")
        if not isinstance(self.p2p_adapter, NetworkBackendAdapterContract):
            raise TypeError("p2p_adapter must be NetworkBackendAdapterContract")
        if self.p2p_adapter.adapter_id != "net_p2p_mesh_adapter":
            raise ValueError("p2p_adapter must bind to net_p2p_mesh_adapter")
        if not isinstance(self.disable_policy, VpnPolicyDisableContract):
            raise TypeError("disable_policy must be VpnPolicyDisableContract")
        if self.disable_policy.p2p_mesh_disabled is not True:
            raise ValueError("canonical disable policy must keep p2p_mesh_disabled true")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_authority_allowed": self.direct_core_authority_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "mesh_id": self.mesh_id,
            "owner_surface": self.owner_surface,
            "p2p_adapter": _to_dict(self.p2p_adapter),
            "disable_policy": self.disable_policy.to_dict(),
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_authority_allowed": self.direct_core_authority_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def get_p2p_mesh_adapter() -> NetworkBackendAdapterContract:
    registry = build_default_network_backend_adapter_registry()
    for adapter in registry.adapters:
        if adapter.adapter_id == "net_p2p_mesh_adapter":
            return adapter
    raise RuntimeError("net_p2p_mesh_adapter is missing from canonical adapter registry")


def build_p2p_mesh_contract() -> P2PMeshContract:
    return P2PMeshContract(
        schema_version="p2p_mesh_contract.v1",
        mesh_id="shared_mobile_p2p_mesh_disabled_default",
        owner_surface="shared_mobile_core/p2p_mesh_network",
        p2p_adapter=get_p2p_mesh_adapter(),
        disable_policy=build_default_vpn_policy_disable_contract(),
        p2p_mesh_disabled=True,
        real_p2p_networking_allowed=False,
        peer_discovery_allowed=False,
        socket_open_allowed=False,
        ports_opened=False,
        external_network_access_enabled=False,
        tunnel_creation_allowed=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_authority_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=("p2p_mesh_contract_binds_existing_net_p2p_mesh_adapter",),
    )
