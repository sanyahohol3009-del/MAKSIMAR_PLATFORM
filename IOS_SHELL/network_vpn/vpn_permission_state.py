from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


IosVpnPermissionStatus = Literal["not_requested", "observed_only", "blocked_by_policy"]


@dataclass(frozen=True, slots=True)
class IosVpnPermissionState:
    """Observed iOS VPN permission state.

    This does not request iOS permission and does not call NetworkExtension or NEVPN APIs.
    """

    schema_version: str
    permission_state_id: str
    platform: str
    status: IosVpnPermissionStatus
    permission_declared: bool
    permission_granted: bool
    permission_prompt_allowed: bool
    permission_prompt_executed: bool
    system_api_call_allowed: bool
    network_extension_api_call_allowed: bool
    nevpn_api_call_allowed: bool
    ios_intent_emitted: bool
    user_interaction_required: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    runtime_mutation_allowed: bool
    dashboard_visible: bool
    read_only: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "ios_vpn_permission_state.v1":
            raise ValueError("schema_version must be ios_vpn_permission_state.v1")
        if self.permission_state_id != "ios_vpn_permission_state_blocked_default":
            raise ValueError("permission_state_id must be ios_vpn_permission_state_blocked_default")
        if self.platform != "ios":
            raise ValueError("platform must be ios")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "user_interaction_required": self.user_interaction_required,
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
            "permission_declared": self.permission_declared,
            "permission_granted": self.permission_granted,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "permission_prompt_executed": self.permission_prompt_executed,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "ios_intent_emitted": self.ios_intent_emitted,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "permission_state_id": self.permission_state_id,
            "platform": self.platform,
            "status": self.status,
            "permission_declared": self.permission_declared,
            "permission_granted": self.permission_granted,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "permission_prompt_executed": self.permission_prompt_executed,
            "system_api_call_allowed": self.system_api_call_allowed,
            "network_extension_api_call_allowed": self.network_extension_api_call_allowed,
            "nevpn_api_call_allowed": self.nevpn_api_call_allowed,
            "ios_intent_emitted": self.ios_intent_emitted,
            "user_interaction_required": self.user_interaction_required,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_ios_vpn_permission_state() -> IosVpnPermissionState:
    return IosVpnPermissionState(
        schema_version="ios_vpn_permission_state.v1",
        permission_state_id="ios_vpn_permission_state_blocked_default",
        platform="ios",
        status="blocked_by_policy",
        permission_declared=False,
        permission_granted=False,
        permission_prompt_allowed=False,
        permission_prompt_executed=False,
        system_api_call_allowed=False,
        network_extension_api_call_allowed=False,
        nevpn_api_call_allowed=False,
        ios_intent_emitted=False,
        user_interaction_required=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        runtime_mutation_allowed=False,
        dashboard_visible=True,
        read_only=True,
        containerization_ready=True,
        reason_codes=("ios_vpn_permission_prompt_blocked_until_control_plane_approval",),
    )
