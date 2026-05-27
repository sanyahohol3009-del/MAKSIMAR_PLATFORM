from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.network_backend_adapter_contract import (
    NetworkBackendAdapterRegistry,
    build_default_network_backend_adapter_registry,
)


@dataclass(frozen=True, slots=True)
class VpnPolicyDisableContract:
    """Global policy-disable contract for VPN/P2P network security runtime."""

    schema_version: str
    policy_id: str
    runtime_disabled_by_default: bool
    server_vpn_disabled: bool
    mobile_vpn_disabled: bool
    p2p_mesh_disabled: bool
    egress_guard_enforce_only: bool
    dashboard_visible: bool
    disable_safe: bool
    policy_disable_supported: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    network_egress_allowed_by_default: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "vpn_policy_disable_contract.v1":
            raise ValueError("schema_version must be vpn_policy_disable_contract.v1")
        if self.policy_id != "phase_2_vpn_policy_disable_contract":
            raise ValueError("policy_id must be phase_2_vpn_policy_disable_contract")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

        required_true = {
            "runtime_disabled_by_default": self.runtime_disabled_by_default,
            "server_vpn_disabled": self.server_vpn_disabled,
            "mobile_vpn_disabled": self.mobile_vpn_disabled,
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "egress_guard_enforce_only": self.egress_guard_enforce_only,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "network_egress_allowed_by_default": self.network_egress_allowed_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "policy_id": self.policy_id,
            "runtime_disabled_by_default": self.runtime_disabled_by_default,
            "server_vpn_disabled": self.server_vpn_disabled,
            "mobile_vpn_disabled": self.mobile_vpn_disabled,
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "egress_guard_enforce_only": self.egress_guard_enforce_only,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "network_egress_allowed_by_default": self.network_egress_allowed_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(frozen=True, slots=True)
class VpnDisabledRuntimeState:
    """Dashboard-visible disabled VPN runtime state."""

    contract: VpnPolicyDisableContract
    adapter_registry: NetworkBackendAdapterRegistry

    def __post_init__(self) -> None:
        if not isinstance(self.contract, VpnPolicyDisableContract):
            raise TypeError("contract must be VpnPolicyDisableContract")
        if not isinstance(self.adapter_registry, NetworkBackendAdapterRegistry):
            raise TypeError("adapter_registry must be NetworkBackendAdapterRegistry")
        for adapter in self.adapter_registry.adapters:
            if adapter.runtime_implemented:
                raise ValueError(f"disabled VPN state cannot include implemented runtime: {adapter.adapter_id}")
            if adapter.runtime_execution_verified:
                raise ValueError(f"disabled VPN state cannot include verified runtime: {adapter.adapter_id}")
            if adapter.external_network_access_enabled:
                raise ValueError(f"disabled VPN state cannot enable external network: {adapter.adapter_id}")
            if adapter.ports_opened or adapter.containers_started:
                raise ValueError(f"disabled VPN state cannot open ports or start containers: {adapter.adapter_id}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": self.contract.to_dict(),
            "adapter_registry": self.adapter_registry.to_dict(),
            "dashboard_visible": True,
            "runtime_disabled": True,
            "containerization_ready": True,
            "ports_opened": False,
            "containers_started": False,
            "active_deployment_created": False,
        }


def build_default_vpn_policy_disable_contract() -> VpnPolicyDisableContract:
    return VpnPolicyDisableContract(
        schema_version="vpn_policy_disable_contract.v1",
        policy_id="phase_2_vpn_policy_disable_contract",
        runtime_disabled_by_default=True,
        server_vpn_disabled=True,
        mobile_vpn_disabled=True,
        p2p_mesh_disabled=True,
        egress_guard_enforce_only=True,
        dashboard_visible=True,
        disable_safe=True,
        policy_disable_supported=True,
        runtime_mutation_allowed=False,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
        network_egress_allowed_by_default=False,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        containerization_ready=True,
        reason_codes=(
            "network_runtime_disabled_until_policy_gate",
            "no_external_network_access_by_default",
            "containerization_ready_reference_only",
        ),
    )


def build_default_vpn_disabled_runtime_state() -> VpnDisabledRuntimeState:
    return VpnDisabledRuntimeState(
        contract=build_default_vpn_policy_disable_contract(),
        adapter_registry=build_default_network_backend_adapter_registry(),
    )
