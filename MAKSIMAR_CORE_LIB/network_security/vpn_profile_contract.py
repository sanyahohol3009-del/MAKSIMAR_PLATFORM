from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal


VpnProfileKind = Literal["server_managed", "mobile_managed", "p2p_managed"]
VpnProfileStatus = Literal["disabled", "configured_reference", "policy_ready"]
VpnTransportKind = Literal["wireguard_candidate", "system_vpn_candidate", "p2p_overlay_candidate"]

_PROFILE_ID_PATTERN = re.compile(r"^vpn_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be non-empty")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class VpnProfileContract:
    """VPN profile declaration.

    This contract does not create a VPN tunnel and does not contain credentials.
    """

    profile_id: str
    profile_kind: VpnProfileKind
    status: VpnProfileStatus
    transport_kind: VpnTransportKind
    owner_scope: str
    requires_operator_approval: bool
    credential_material_present: bool
    secret_material_embedded: bool
    tunnel_creation_allowed: bool
    network_egress_allowed_by_default: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    dashboard_visible: bool
    disable_safe: bool
    policy_disable_supported: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        profile_id = _ensure_non_empty_str(self.profile_id, "profile_id")
        if not _PROFILE_ID_PATTERN.fullmatch(profile_id):
            raise ValueError(f"invalid profile_id: {profile_id}")
        _ensure_non_empty_str(self.owner_scope, "owner_scope")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "requires_operator_approval": self.requires_operator_approval,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if _ensure_bool(value, field_name) is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "credential_material_present": self.credential_material_present,
            "secret_material_embedded": self.secret_material_embedded,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "network_egress_allowed_by_default": self.network_egress_allowed_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
        for field_name, value in required_false.items():
            if _ensure_bool(value, field_name) is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "profile_kind": self.profile_kind,
            "status": self.status,
            "transport_kind": self.transport_kind,
            "owner_scope": self.owner_scope,
            "requires_operator_approval": self.requires_operator_approval,
            "credential_material_present": self.credential_material_present,
            "secret_material_embedded": self.secret_material_embedded,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "network_egress_allowed_by_default": self.network_egress_allowed_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_default_vpn_profiles() -> tuple[VpnProfileContract, ...]:
    return (
        VpnProfileContract(
            profile_id="vpn_server_profile",
            profile_kind="server_managed",
            status="disabled",
            transport_kind="wireguard_candidate",
            owner_scope="server",
            requires_operator_approval=True,
            credential_material_present=False,
            secret_material_embedded=False,
            tunnel_creation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            containerization_ready=True,
            reason_codes=("server_vpn_profile_disabled_until_policy_gate",),
        ),
        VpnProfileContract(
            profile_id="vpn_mobile_profile",
            profile_kind="mobile_managed",
            status="disabled",
            transport_kind="system_vpn_candidate",
            owner_scope="mobile",
            requires_operator_approval=True,
            credential_material_present=False,
            secret_material_embedded=False,
            tunnel_creation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            containerization_ready=True,
            reason_codes=("mobile_vpn_profile_disabled_until_platform_binding",),
        ),
    )
