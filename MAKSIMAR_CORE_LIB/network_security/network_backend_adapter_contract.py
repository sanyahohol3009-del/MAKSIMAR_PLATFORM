from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal


NetworkBackendKind = Literal[
    "server_vpn",
    "mobile_vpn",
    "p2p_mesh",
    "floating_master",
    "egress_guard",
]

NetworkBackendScope = Literal[
    "server",
    "android",
    "ios",
    "shared_mobile",
    "container",
]

NetworkBackendRuntimeMode = Literal[
    "disabled",
    "read_only_reference",
    "policy_gated_runtime",
]

NetworkContainerProfile = Literal[
    "core_library",
    "server_service",
    "mobile_shell",
    "shared_mobile_core",
    "network_security_cube",
    "not_loaded",
]

_ADAPTER_ID_PATTERN = re.compile(r"^net_[a-z][a-z0-9_]*$")
_PATH_PATTERN = re.compile(r"^[A-Za-z0-9_./-]+$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def _validate_paths(paths: tuple[str, ...], field_name: str, owner_id: str) -> tuple[str, ...]:
    if not isinstance(paths, tuple):
        raise TypeError(f"{field_name} must be a tuple")

    normalized_paths: list[str] = []
    for path in paths:
        normalized = _ensure_non_empty_str(path, field_name)
        if not _PATH_PATTERN.fullmatch(normalized):
            raise ValueError(f"invalid path in {field_name} for {owner_id}: {normalized}")
        if "__pycache__" in normalized or normalized.endswith((".pyc", ".pyo")):
            raise ValueError(f"{field_name} must not reference compiled cache files")
        if normalized.startswith("EXTERNAL_BACKENDS/"):
            raise ValueError(f"{field_name} must not bind directly to external backends")
        normalized_paths.append(normalized)

    if len(set(normalized_paths)) != len(normalized_paths):
        raise ValueError(f"duplicate paths in {field_name} for {owner_id}")

    return tuple(normalized_paths)


@dataclass(frozen=True, slots=True)
class NetworkBackendAdapterContract:
    """Policy-first network backend adapter contract.

    This is not a tunnel implementation. It declares a safe adapter boundary for
    future VPN, P2P, egress and mobile network integrations.
    """

    adapter_id: str
    title: str
    backend_kind: NetworkBackendKind
    scope: NetworkBackendScope
    runtime_mode: NetworkBackendRuntimeMode
    container_profile: NetworkContainerProfile
    owner_surface: str
    contract_paths: tuple[str, ...]
    policy_refs: tuple[str, ...]
    dashboard_visible: bool
    disable_safe: bool
    policy_disable_supported: bool
    runtime_implemented: bool
    runtime_execution_verified: bool
    runtime_evidence_paths: tuple[str, ...]
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    runtime_mutation_allowed: bool
    network_egress_allowed_by_default: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    requires_operator_approval: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        adapter_id = _ensure_non_empty_str(self.adapter_id, "adapter_id")
        if not _ADAPTER_ID_PATTERN.fullmatch(adapter_id):
            raise ValueError(f"invalid adapter_id: {adapter_id}")

        title = _ensure_non_empty_str(self.title, "title")
        owner_surface = _ensure_non_empty_str(self.owner_surface, "owner_surface")

        contract_paths = _validate_paths(self.contract_paths, "contract_paths", adapter_id)
        policy_refs = _validate_paths(self.policy_refs, "policy_refs", adapter_id)
        runtime_evidence_paths = _validate_paths(
            self.runtime_evidence_paths,
            "runtime_evidence_paths",
            adapter_id,
        )
        reason_codes = _validate_paths(self.reason_codes, "reason_codes", adapter_id)

        if not contract_paths:
            raise ValueError(f"contract_paths must not be empty for {adapter_id}")
        if not policy_refs:
            raise ValueError(f"policy_refs must not be empty for {adapter_id}")
        if not reason_codes:
            raise ValueError(f"reason_codes must not be empty for {adapter_id}")

        runtime_implemented = _ensure_bool(self.runtime_implemented, "runtime_implemented")
        runtime_execution_verified = _ensure_bool(
            self.runtime_execution_verified,
            "runtime_execution_verified",
        )

        if self.runtime_mode in {"disabled", "read_only_reference"}:
            if runtime_implemented:
                raise ValueError(f"{self.runtime_mode} cannot be runtime_implemented")
            if runtime_execution_verified:
                raise ValueError(f"{self.runtime_mode} cannot be runtime_execution_verified")
            if runtime_evidence_paths:
                raise ValueError(f"{self.runtime_mode} must not include runtime evidence")

        if self.runtime_mode == "policy_gated_runtime":
            if not self.requires_operator_approval:
                raise ValueError("policy_gated_runtime requires operator approval")
            if runtime_implemented != runtime_execution_verified:
                raise ValueError("runtime implemented/verified flags must move together")

        if not _ensure_bool(self.dashboard_visible, "dashboard_visible"):
            raise ValueError("dashboard_visible must remain true")
        if not _ensure_bool(self.disable_safe, "disable_safe"):
            raise ValueError("disable_safe must remain true")
        if not _ensure_bool(self.policy_disable_supported, "policy_disable_supported"):
            raise ValueError("policy_disable_supported must remain true")
        if _ensure_bool(self.direct_core_import_allowed, "direct_core_import_allowed"):
            raise ValueError("direct_core_import_allowed must remain false")
        if _ensure_bool(self.source_of_truth_override_allowed, "source_of_truth_override_allowed"):
            raise ValueError("source_of_truth_override_allowed must remain false")
        if _ensure_bool(self.runtime_mutation_allowed, "runtime_mutation_allowed"):
            raise ValueError("runtime_mutation_allowed must remain false")
        if _ensure_bool(self.network_egress_allowed_by_default, "network_egress_allowed_by_default"):
            raise ValueError("network_egress_allowed_by_default must remain false")
        if _ensure_bool(self.external_network_access_enabled, "external_network_access_enabled"):
            raise ValueError("external_network_access_enabled must remain false")
        if _ensure_bool(self.ports_opened, "ports_opened"):
            raise ValueError("ports_opened must remain false")
        if _ensure_bool(self.containers_started, "containers_started"):
            raise ValueError("containers_started must remain false")
        if _ensure_bool(self.active_deployment_created, "active_deployment_created"):
            raise ValueError("active_deployment_created must remain false")
        if not _ensure_bool(self.containerization_ready, "containerization_ready"):
            raise ValueError("containerization_ready must remain true")

        object.__setattr__(self, "adapter_id", adapter_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "owner_surface", owner_surface)
        object.__setattr__(self, "contract_paths", contract_paths)
        object.__setattr__(self, "policy_refs", policy_refs)
        object.__setattr__(self, "runtime_evidence_paths", runtime_evidence_paths)
        object.__setattr__(self, "reason_codes", reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "title": self.title,
            "backend_kind": self.backend_kind,
            "scope": self.scope,
            "runtime_mode": self.runtime_mode,
            "container_profile": self.container_profile,
            "owner_surface": self.owner_surface,
            "contract_paths": list(self.contract_paths),
            "policy_refs": list(self.policy_refs),
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "runtime_implemented": self.runtime_implemented,
            "runtime_execution_verified": self.runtime_execution_verified,
            "runtime_evidence_paths": list(self.runtime_evidence_paths),
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "network_egress_allowed_by_default": self.network_egress_allowed_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "requires_operator_approval": self.requires_operator_approval,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(frozen=True, slots=True)
class NetworkBackendAdapterRegistry:
    schema_version: str
    registry_id: str
    adapters: tuple[NetworkBackendAdapterContract, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "network_backend_adapter_contract.v1":
            raise ValueError("schema_version must be network_backend_adapter_contract.v1")
        if self.registry_id != "phase_2_network_backend_adapter_registry":
            raise ValueError("registry_id must be phase_2_network_backend_adapter_registry")
        if not isinstance(self.adapters, tuple):
            raise TypeError("adapters must be a tuple")
        if not self.adapters:
            raise ValueError("adapters must not be empty")

        adapter_ids = tuple(adapter.adapter_id for adapter in self.adapters)
        if len(set(adapter_ids)) != len(adapter_ids):
            raise ValueError("duplicate adapter_id values detected")

        for adapter in self.adapters:
            if not isinstance(adapter, NetworkBackendAdapterContract):
                raise TypeError("adapters must contain NetworkBackendAdapterContract")
            if not adapter.containerization_ready:
                raise ValueError(f"adapter is not containerization-ready: {adapter.adapter_id}")
            if adapter.ports_opened or adapter.containers_started:
                raise ValueError(f"adapter must not open ports or start containers: {adapter.adapter_id}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_id": self.registry_id,
            "adapters": [adapter.to_dict() for adapter in self.adapters],
        }


def build_default_network_backend_adapter_registry() -> NetworkBackendAdapterRegistry:
    common_contract_paths = (
        "MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py",
    )
    common_policy_refs = (
        "MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py",
        "MAKSIMAR_CORE_LIB/network_containerization/container_exposure_policy.py",
        "MAKSIMAR_CORE_LIB/network_trust_boundaries/network_trust_boundaries_contract.py",
    )

    adapters = (
        NetworkBackendAdapterContract(
            adapter_id="net_server_vpn_adapter",
            title="Server VPN Adapter Boundary",
            backend_kind="server_vpn",
            scope="server",
            runtime_mode="disabled",
            container_profile="server_service",
            owner_surface="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
            contract_paths=common_contract_paths,
            policy_refs=common_policy_refs,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("server_vpn_disabled_until_policy_approval",),
        ),
        NetworkBackendAdapterContract(
            adapter_id="net_mobile_vpn_adapter",
            title="Mobile VPN Adapter Boundary",
            backend_kind="mobile_vpn",
            scope="shared_mobile",
            runtime_mode="disabled",
            container_profile="shared_mobile_core",
            owner_surface="shared_mobile_core/network_vpn",
            contract_paths=common_contract_paths,
            policy_refs=common_policy_refs,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("mobile_vpn_disabled_until_platform_binding",),
        ),
        NetworkBackendAdapterContract(
            adapter_id="net_p2p_mesh_adapter",
            title="P2P Mesh Adapter Boundary",
            backend_kind="p2p_mesh",
            scope="shared_mobile",
            runtime_mode="disabled",
            container_profile="shared_mobile_core",
            owner_surface="shared_mobile_core/p2p_mesh_network",
            contract_paths=common_contract_paths,
            policy_refs=common_policy_refs,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("p2p_mesh_disabled_until_owner_approval",),
        ),
        NetworkBackendAdapterContract(
            adapter_id="net_egress_guard_adapter",
            title="Egress Guard Adapter Boundary",
            backend_kind="egress_guard",
            scope="server",
            runtime_mode="read_only_reference",
            container_profile="network_security_cube",
            owner_surface="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
            contract_paths=common_contract_paths,
            policy_refs=common_policy_refs,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("egress_guard_read_only_reference_until_runtime_batch",),
        ),
    )

    return NetworkBackendAdapterRegistry(
        schema_version="network_backend_adapter_contract.v1",
        registry_id="phase_2_network_backend_adapter_registry",
        adapters=adapters,
    )
