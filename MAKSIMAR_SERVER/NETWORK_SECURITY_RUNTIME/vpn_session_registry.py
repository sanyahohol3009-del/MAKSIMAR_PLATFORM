from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.vpn_session_contract import (
    VpnSessionContract,
    build_disabled_vpn_session,
)


@dataclass(frozen=True, slots=True)
class VpnSessionRegistry:
    """Read-only VPN session registry for server runtime visibility."""

    schema_version: str
    registry_id: str
    sessions: tuple[VpnSessionContract, ...]
    runtime_started: bool
    tunnel_created: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    dashboard_visible: bool
    containerization_ready: bool

    def __post_init__(self) -> None:
        if self.schema_version != "vpn_session_registry.v1":
            raise ValueError("schema_version must be vpn_session_registry.v1")
        if self.registry_id != "phase_2_vpn_session_registry":
            raise ValueError("registry_id must be phase_2_vpn_session_registry")
        if not isinstance(self.sessions, tuple) or not self.sessions:
            raise ValueError("sessions must be a non-empty tuple")

        for session in self.sessions:
            if not isinstance(session, VpnSessionContract):
                raise TypeError("sessions must contain VpnSessionContract")
            if session.started or session.connected or session.tunnel_active or session.egress_active:
                raise ValueError("registry cannot contain active sessions in disabled runtime")
            if session.ports_opened or session.containers_started or session.active_deployment_created:
                raise ValueError("registry sessions must not open ports/start containers/deploy")

        required_false = {
            "runtime_started": self.runtime_started,
            "tunnel_created": self.tunnel_created,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

        if self.dashboard_visible is not True:
            raise ValueError("dashboard_visible must remain true")
        if self.containerization_ready is not True:
            raise ValueError("containerization_ready must remain true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_id": self.registry_id,
            "sessions": [session.to_dict() for session in self.sessions],
            "runtime_started": self.runtime_started,
            "tunnel_created": self.tunnel_created,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
        }


def build_default_vpn_session_registry() -> VpnSessionRegistry:
    return VpnSessionRegistry(
        schema_version="vpn_session_registry.v1",
        registry_id="phase_2_vpn_session_registry",
        sessions=(build_disabled_vpn_session(),),
        runtime_started=False,
        tunnel_created=False,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
        dashboard_visible=True,
        containerization_ready=True,
    )
