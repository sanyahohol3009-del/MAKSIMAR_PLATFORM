from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.egress_policy_contract import (
    EgressPolicyContract,
    build_default_egress_policy_contract,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnPolicyDisableContract,
    build_default_vpn_policy_disable_contract,
)

from ANDROID_SHELL.network_vpn.vpn_permission_state import (
    AndroidVpnPermissionState,
    build_android_vpn_permission_state,
)
from ANDROID_SHELL.network_vpn.vpn_profile_models import (
    AndroidVpnProfileModel,
    build_android_vpn_profile_model,
)
from ANDROID_SHELL.network_vpn.vpn_state_bridge import (
    AndroidVpnStateBridge,
    build_android_vpn_state_bridge,
)
from ANDROID_SHELL.network_vpn.vpn_sync_contract import (
    AndroidVpnSyncContract,
    build_android_vpn_sync_contract,
)


@dataclass(frozen=True, slots=True)
class AndroidVpnPolicyBinding:
    """Android VPN shell policy binding.

    Binds Android shell VPN projection to canonical network security policy.
    """

    schema_version: str
    binding_id: str
    platform: str
    profile: AndroidVpnProfileModel
    permission_state: AndroidVpnPermissionState
    state_bridge: AndroidVpnStateBridge
    sync_contract: AndroidVpnSyncContract
    vpn_policy: VpnPolicyDisableContract
    egress_policy: EgressPolicyContract
    android_shell_binding_ready: bool
    source_of_truth_layer: str
    runtime_layer: str
    shell_layer: str
    policy_disabled: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    system_api_call_allowed: bool
    permission_prompt_allowed: bool
    tunnel_creation_allowed: bool
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
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "android_vpn_policy_binding.v1":
            raise ValueError("schema_version must be android_vpn_policy_binding.v1")
        if self.binding_id != "android_vpn_policy_binding_disabled_default":
            raise ValueError("binding_id must be android_vpn_policy_binding_disabled_default")
        if self.platform != "android":
            raise ValueError("platform must be android")
        if not isinstance(self.profile, AndroidVpnProfileModel):
            raise TypeError("profile must be AndroidVpnProfileModel")
        if not isinstance(self.permission_state, AndroidVpnPermissionState):
            raise TypeError("permission_state must be AndroidVpnPermissionState")
        if not isinstance(self.state_bridge, AndroidVpnStateBridge):
            raise TypeError("state_bridge must be AndroidVpnStateBridge")
        if not isinstance(self.sync_contract, AndroidVpnSyncContract):
            raise TypeError("sync_contract must be AndroidVpnSyncContract")
        if not isinstance(self.vpn_policy, VpnPolicyDisableContract):
            raise TypeError("vpn_policy must be VpnPolicyDisableContract")
        if not isinstance(self.egress_policy, EgressPolicyContract):
            raise TypeError("egress_policy must be EgressPolicyContract")
        if self.source_of_truth_layer != "MAKSIMAR_CORE_LIB/network_security":
            raise ValueError("source_of_truth_layer must remain canonical network_security")
        if self.runtime_layer != "MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME":
            raise ValueError("runtime_layer must remain NETWORK_SECURITY_RUNTIME")
        if self.shell_layer != "ANDROID_SHELL/network_vpn":
            raise ValueError("shell_layer must be ANDROID_SHELL/network_vpn")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "android_shell_binding_ready": self.android_shell_binding_ready,
            "policy_disabled": self.policy_disabled,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "system_api_call_allowed": self.system_api_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
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
            "binding_id": self.binding_id,
            "platform": self.platform,
            "profile": self.profile.to_dict(),
            "permission_state": self.permission_state.to_dict(),
            "state_bridge": self.state_bridge.to_dict(),
            "sync_contract": self.sync_contract.to_dict(),
            "vpn_policy": self.vpn_policy.to_dict(),
            "egress_policy": self.egress_policy.to_dict(),
            "android_shell_binding_ready": self.android_shell_binding_ready,
            "source_of_truth_layer": self.source_of_truth_layer,
            "runtime_layer": self.runtime_layer,
            "shell_layer": self.shell_layer,
            "policy_disabled": self.policy_disabled,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "system_api_call_allowed": self.system_api_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
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
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_android_vpn_policy_binding() -> AndroidVpnPolicyBinding:
    return AndroidVpnPolicyBinding(
        schema_version="android_vpn_policy_binding.v1",
        binding_id="android_vpn_policy_binding_disabled_default",
        platform="android",
        profile=build_android_vpn_profile_model(),
        permission_state=build_android_vpn_permission_state(),
        state_bridge=build_android_vpn_state_bridge(),
        sync_contract=build_android_vpn_sync_contract(),
        vpn_policy=build_default_vpn_policy_disable_contract(),
        egress_policy=build_default_egress_policy_contract(),
        android_shell_binding_ready=True,
        source_of_truth_layer="MAKSIMAR_CORE_LIB/network_security",
        runtime_layer="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
        shell_layer="ANDROID_SHELL/network_vpn",
        policy_disabled=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        system_api_call_allowed=False,
        permission_prompt_allowed=False,
        tunnel_creation_allowed=False,
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
        containerization_ready=True,
        reason_codes=(
            "android_vpn_shell_binding_ready",
            "canonical_network_security_policy_reused",
            "no_android_vpn_api_execution",
        ),
    )
