from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal


VpnSessionState = Literal["disabled", "not_started", "policy_blocked", "terminated"]
_SESSION_ID_PATTERN = re.compile(r"^vpn_session_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class VpnSessionContract:
    """VPN session state contract.

    It models lifecycle state only. It does not start a tunnel.
    """

    session_id: str
    profile_id: str
    state: VpnSessionState
    started: bool
    connected: bool
    tunnel_active: bool
    egress_active: bool
    runtime_execution_verified: bool
    runtime_mutation_allowed: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    dashboard_visible: bool
    disable_safe: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, str) or not _SESSION_ID_PATTERN.fullmatch(self.session_id):
            raise ValueError("invalid session_id")
        if not isinstance(self.profile_id, str) or not self.profile_id.startswith("vpn_"):
            raise ValueError("profile_id must reference a vpn profile")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_false = {
            "started": self.started,
            "connected": self.connected,
            "tunnel_active": self.tunnel_active,
            "egress_active": self.egress_active,
            "runtime_execution_verified": self.runtime_execution_verified,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false in contract batch")

        required_true = {
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "profile_id": self.profile_id,
            "state": self.state,
            "started": self.started,
            "connected": self.connected,
            "tunnel_active": self.tunnel_active,
            "egress_active": self.egress_active,
            "runtime_execution_verified": self.runtime_execution_verified,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_disabled_vpn_session(profile_id: str = "vpn_server_profile") -> VpnSessionContract:
    return VpnSessionContract(
        session_id="vpn_session_disabled_default",
        profile_id=profile_id,
        state="disabled",
        started=False,
        connected=False,
        tunnel_active=False,
        egress_active=False,
        runtime_execution_verified=False,
        runtime_mutation_allowed=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        dashboard_visible=True,
        disable_safe=True,
        containerization_ready=True,
        reason_codes=("vpn_session_disabled_by_policy",),
    )
