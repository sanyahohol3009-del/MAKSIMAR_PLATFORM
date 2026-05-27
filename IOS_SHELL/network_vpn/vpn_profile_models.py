from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.vpn_profile_contract import (
    VpnProfileContract,
    build_default_vpn_profiles,
)


@dataclass(frozen=True, slots=True)
class IosVpnProfileModel:
    """iOS shell projection of the canonical mobile VPN profile."""

    schema_version: str
    profile_id: str
    ios_profile_id: str
    canonical_profile: VpnProfileContract
    shell_surface: str
    platform: str
    profile_visible: bool
    profile_editable_from_ios: bool
    system_api_call_allowed: bool
    network_extension_api_call_allowed: bool
    nevpn_api_call_allowed: bool
    tunnel_creation_allowed: bool
    permission_prompt_allowed: bool
    secret_material_embedded: bool
    credential_material_present: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    source_of_truth_override_allowed: bool
    direct_core_import_allowed: bool
    dashboard_visible: bool
    read_only: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "ios_vpn_profile_model.v1":
            raise ValueError("schema_version must be ios_vpn_profile_model.v1")
        if self.platform != "ios":
            raise ValueError("platform must be ios")
        if self.shell_surface != "IOS_SHELL/network_vpn":
            raise ValueError("shell_surface must be IOS_SHELL/network_vpn")
        if not isinstance(self.canonical_profile, VpnProfileContract):
            raise TypeError("canonical_profile must be VpnProfileContract")
        if self.canonical_profile.profile_id != "vpn_mobile_profile":
            raise ValueError("iOS VPN profile must bind to vpn_mobile_profile")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "profile_visible": self.profile_visible,
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
            "profile_editable_from_ios": self.profile_editable_from_ios,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "secret_material_embedded": self.secret_material_embedded,
            "credential_material_present": self.credential_material_present,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "ios_profile_id": self.ios_profile_id,
            "canonical_profile": self.canonical_profile.to_dict(),
            "shell_surface": self.shell_surface,
            "platform": self.platform,
            "profile_visible": self.profile_visible,
            "profile_editable_from_ios": self.profile_editable_from_ios,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "secret_material_embedded": self.secret_material_embedded,
            "credential_material_present": self.credential_material_present,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def _get_mobile_profile() -> VpnProfileContract:
    for profile in build_default_vpn_profiles():
        if profile.profile_id == "vpn_mobile_profile":
            return profile
    raise RuntimeError("vpn_mobile_profile is missing from canonical VPN profiles")


def build_ios_vpn_profile_model() -> IosVpnProfileModel:
    return IosVpnProfileModel(
        schema_version="ios_vpn_profile_model.v1",
        profile_id="vpn_mobile_profile",
        ios_profile_id="ios_vpn_mobile_profile_projection",
        canonical_profile=_get_mobile_profile(),
        shell_surface="IOS_SHELL/network_vpn",
        platform="ios",
        profile_visible=True,
        profile_editable_from_ios=False,
        system_api_call_allowed=False,
        network_extension_api_call_allowed=False,
        nevpn_api_call_allowed=False,
        tunnel_creation_allowed=False,
        permission_prompt_allowed=False,
        secret_material_embedded=False,
        credential_material_present=False,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_import_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=("ios_vpn_profile_projection_uses_canonical_mobile_profile",),
    )
