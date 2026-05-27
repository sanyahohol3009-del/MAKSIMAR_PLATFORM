from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.mobile_vpn_hook_contract import (
    MobileVpnHookContract,
    build_default_mobile_vpn_hooks,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_session_contract import (
    VpnSessionContract,
    build_disabled_vpn_session,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_status_read_model import (
    VpnStatusReadModel,
    build_default_vpn_status_read_model,
)

from IOS_SHELL.network_vpn.vpn_permission_state import (
    IosVpnPermissionState,
    build_ios_vpn_permission_state,
)
from IOS_SHELL.network_vpn.vpn_profile_models import (
    IosVpnProfileModel,
    build_ios_vpn_profile_model,
)


@dataclass(frozen=True, slots=True)
class IosVpnStateBridge:
    """iOS shell bridge for VPN status.

    Bridges canonical disabled/read-only VPN state into iOS shell projection.
    """

    schema_version: str
    bridge_id: str
    platform: str
    profile: IosVpnProfileModel
    permission_state: IosVpnPermissionState
    mobile_hook: MobileVpnHookContract
    vpn_status: VpnStatusReadModel
    session: VpnSessionContract
    bridge_active: bool
    tunnel_active: bool
    connected: bool
    system_api_call_allowed: bool
    network_extension_api_call_allowed: bool
    nevpn_api_call_allowed: bool
    permission_prompt_allowed: bool
    permission_prompt_executed: bool
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
        if self.schema_version != "ios_vpn_state_bridge.v1":
            raise ValueError("schema_version must be ios_vpn_state_bridge.v1")
        if self.bridge_id != "ios_vpn_state_bridge_disabled_default":
            raise ValueError("bridge_id must be ios_vpn_state_bridge_disabled_default")
        if self.platform != "ios":
            raise ValueError("platform must be ios")
        if not isinstance(self.profile, IosVpnProfileModel):
            raise TypeError("profile must be IosVpnProfileModel")
        if not isinstance(self.permission_state, IosVpnPermissionState):
            raise TypeError("permission_state must be IosVpnPermissionState")
        if not isinstance(self.mobile_hook, MobileVpnHookContract):
            raise TypeError("mobile_hook must be MobileVpnHookContract")
        if self.mobile_hook.platform != "ios":
            raise ValueError("mobile_hook must be ios hook")
        if not isinstance(self.vpn_status, VpnStatusReadModel):
            raise TypeError("vpn_status must be VpnStatusReadModel")
        if not isinstance(self.session, VpnSessionContract):
            raise TypeError("session must be VpnSessionContract")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
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
            "bridge_active": self.bridge_active,
            "tunnel_active": self.tunnel_active,
            "connected": self.connected,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "permission_prompt_executed": self.permission_prompt_executed,
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
            "bridge_id": self.bridge_id,
            "platform": self.platform,
            "profile": self.profile.to_dict(),
            "permission_state": self.permission_state.to_dict(),
            "mobile_hook": self.mobile_hook.to_dict(),
            "vpn_status": self.vpn_status.to_dict(),
            "session": self.session.to_dict(),
            "bridge_active": self.bridge_active,
            "tunnel_active": self.tunnel_active,
            "connected": self.connected,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "permission_prompt_executed": self.permission_prompt_executed,
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


def _get_ios_mobile_hook() -> MobileVpnHookContract:
    for hook in build_default_mobile_vpn_hooks():
        if hook.platform == "ios":
            return hook
    raise RuntimeError("ios mobile VPN hook is missing")


def build_ios_vpn_state_bridge() -> IosVpnStateBridge:
    return IosVpnStateBridge(
        schema_version="ios_vpn_state_bridge.v1",
        bridge_id="ios_vpn_state_bridge_disabled_default",
        platform="ios",
        profile=build_ios_vpn_profile_model(),
        permission_state=build_ios_vpn_permission_state(),
        mobile_hook=_get_ios_mobile_hook(),
        vpn_status=build_default_vpn_status_read_model(),
        session=build_disabled_vpn_session(profile_id="vpn_mobile_profile"),
        bridge_active=False,
        tunnel_active=False,
        connected=False,
        system_api_call_allowed=False,
        network_extension_api_call_allowed=False,
        nevpn_api_call_allowed=False,
        permission_prompt_allowed=False,
        permission_prompt_executed=False,
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
        reason_codes=("ios_vpn_state_bridge_projects_canonical_disabled_vpn_state",),
    )
