from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_PLATFORMS: tuple[str, ...] = ("android", "ios")
_ALLOWED_OBSERVER_STATES: tuple[str, ...] = (
    "not_connected",
    "consent_required",
    "observing_metadata",
    "paused",
    "blocked",
)
_ALLOWED_CONSENT_STATES: tuple[str, ...] = (
    "consent_required",
    "consent_granted",
    "consent_revoked",
    "blocked",
)
_ALLOWED_REMOTE_ASSISTANCE_STATES: tuple[str, ...] = (
    "disabled",
    "approval_required",
    "approved_intent_pending",
    "rejected",
)


@dataclass(frozen=True)
class PhoneScreenWindowReadModel:
    window_id: str
    panel_id: str
    device_id: str
    owner_identity_id: str
    platform: str
    dashboard_section: str
    observer_state: str
    consent_state: str
    frame_ref: str
    frame_reference_only: bool
    read_only: bool
    remote_assistance_state: str
    remote_assistance_requires_approval: bool
    dashboard_control_allowed: bool
    direct_execution_allowed: bool
    child_control_surface: bool
    family_children_surface_required: bool
    audit_visible: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in (
            "window_id",
            "panel_id",
            "device_id",
            "owner_identity_id",
            "platform",
            "dashboard_section",
            "observer_state",
            "consent_state",
            "frame_ref",
            "remote_assistance_state",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.platform not in _ALLOWED_PLATFORMS:
            raise ValueError(f"unsupported platform: {self.platform}")
        if self.dashboard_section != "Phone Window":
            raise ValueError("dashboard_section must be Phone Window")
        if self.observer_state not in _ALLOWED_OBSERVER_STATES:
            raise ValueError(f"unsupported observer_state: {self.observer_state}")
        if self.consent_state not in _ALLOWED_CONSENT_STATES:
            raise ValueError(f"unsupported consent_state: {self.consent_state}")
        if self.remote_assistance_state not in _ALLOWED_REMOTE_ASSISTANCE_STATES:
            raise ValueError(f"unsupported remote_assistance_state: {self.remote_assistance_state}")
        if not self.frame_reference_only:
            raise ValueError("frame_reference_only must be True")
        if not self.read_only:
            raise ValueError("Phone Screen Window read model must be read-only")
        if not self.remote_assistance_requires_approval:
            raise ValueError("remote_assistance_requires_approval must be True")
        if self.dashboard_control_allowed:
            raise ValueError("dashboard_control_allowed must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.child_control_surface:
            raise ValueError("child_control_surface must be False for Phone Window")
        if not self.family_children_surface_required:
            raise ValueError("family_children_surface_required must be True")
        if not self.audit_visible:
            raise ValueError("audit_visible must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    def to_dict(self) -> dict[str, object]:
        return {
            "window_id": self.window_id,
            "panel_id": self.panel_id,
            "device_id": self.device_id,
            "owner_identity_id": self.owner_identity_id,
            "platform": self.platform,
            "dashboard_section": self.dashboard_section,
            "observer_state": self.observer_state,
            "consent_state": self.consent_state,
            "frame_ref": self.frame_ref,
            "frame_reference_only": self.frame_reference_only,
            "read_only": self.read_only,
            "remote_assistance_state": self.remote_assistance_state,
            "remote_assistance_requires_approval": self.remote_assistance_requires_approval,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "child_control_surface": self.child_control_surface,
            "family_children_surface_required": self.family_children_surface_required,
            "audit_visible": self.audit_visible,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }


def build_default_phone_screen_window_read_model(
    *,
    window_id: str,
    panel_id: str,
    device_id: str,
    owner_identity_id: str,
    platform: str,
    frame_ref: str,
) -> PhoneScreenWindowReadModel:
    return PhoneScreenWindowReadModel(
        window_id=window_id,
        panel_id=panel_id,
        device_id=device_id,
        owner_identity_id=owner_identity_id,
        platform=platform,
        dashboard_section="Phone Window",
        observer_state="observing_metadata",
        consent_state="consent_granted",
        frame_ref=frame_ref,
        frame_reference_only=True,
        read_only=True,
        remote_assistance_state="approval_required",
        remote_assistance_requires_approval=True,
        dashboard_control_allowed=False,
        direct_execution_allowed=False,
        child_control_surface=False,
        family_children_surface_required=True,
        audit_visible=True,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
        source_of_truth_override_allowed=False,
    )
