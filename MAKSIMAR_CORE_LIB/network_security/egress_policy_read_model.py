from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


EgressStatusViewState = Literal["deny_by_default", "policy_blocked"]


@dataclass(frozen=True, slots=True)
class EgressPolicyReadModel:
    """Dashboard-safe network egress read model."""

    schema_version: str
    view_id: str
    status: EgressStatusViewState
    deny_by_default: bool
    external_egress_allowed: bool
    dns_resolution_allowed: bool
    public_ingress_allowed: bool
    tunnel_creation_allowed: bool
    external_connection_attempted: bool
    dns_resolution_performed: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    dashboard_visible: bool
    read_only: bool
    action_buttons_enabled: bool
    control_plane_handoff_required: bool
    audit_required: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "egress_policy_read_model.v1":
            raise ValueError("schema_version must be egress_policy_read_model.v1")
        if self.view_id != "phase_2_egress_policy_read_model":
            raise ValueError("view_id must be phase_2_egress_policy_read_model")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "deny_by_default": self.deny_by_default,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "audit_required": self.audit_required,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "external_egress_allowed": self.external_egress_allowed,
            "dns_resolution_allowed": self.dns_resolution_allowed,
            "public_ingress_allowed": self.public_ingress_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "external_connection_attempted": self.external_connection_attempted,
            "dns_resolution_performed": self.dns_resolution_performed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "action_buttons_enabled": self.action_buttons_enabled,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "view_id": self.view_id,
            "status": self.status,
            "deny_by_default": self.deny_by_default,
            "external_egress_allowed": self.external_egress_allowed,
            "dns_resolution_allowed": self.dns_resolution_allowed,
            "public_ingress_allowed": self.public_ingress_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "external_connection_attempted": self.external_connection_attempted,
            "dns_resolution_performed": self.dns_resolution_performed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "action_buttons_enabled": self.action_buttons_enabled,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "audit_required": self.audit_required,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_default_egress_policy_read_model() -> EgressPolicyReadModel:
    return EgressPolicyReadModel(
        schema_version="egress_policy_read_model.v1",
        view_id="phase_2_egress_policy_read_model",
        status="deny_by_default",
        deny_by_default=True,
        external_egress_allowed=False,
        dns_resolution_allowed=False,
        public_ingress_allowed=False,
        tunnel_creation_allowed=False,
        external_connection_attempted=False,
        dns_resolution_performed=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        dashboard_visible=True,
        read_only=True,
        action_buttons_enabled=False,
        control_plane_handoff_required=True,
        audit_required=True,
        containerization_ready=True,
        reason_codes=("egress_status_visible_read_only_until_policy_gate",),
    )
