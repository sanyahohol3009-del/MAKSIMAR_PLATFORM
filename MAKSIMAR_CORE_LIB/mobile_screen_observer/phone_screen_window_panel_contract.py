from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PhoneScreenWindowPanelContract:
    panel_id: str
    panel_kind: str
    dashboard_section: str
    source_binding: str
    read_model_binding: str
    read_only_default: bool
    can_show_frame_reference: bool
    can_show_consent_state: bool
    can_show_remote_assistance_intent: bool
    can_show_audit_state: bool
    dashboard_direct_execution_allowed: bool
    device_control_execution_allowed: bool
    child_control_allowed: bool
    family_children_surface_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("panel_id", "panel_kind", "dashboard_section", "source_binding", "read_model_binding"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.panel_kind != "phone_screen_window":
            raise ValueError("panel_kind must be phone_screen_window")
        if self.dashboard_section != "Phone Window":
            raise ValueError("dashboard_section must be Phone Window")
        if self.source_binding != "mobile_screen_observer":
            raise ValueError("source_binding must be mobile_screen_observer")
        if self.read_model_binding != "PhoneScreenWindowReadModel":
            raise ValueError("read_model_binding must be PhoneScreenWindowReadModel")
        if not self.read_only_default:
            raise ValueError("read_only_default must be True")
        if not self.can_show_frame_reference:
            raise ValueError("can_show_frame_reference must be True")
        if not self.can_show_consent_state:
            raise ValueError("can_show_consent_state must be True")
        if not self.can_show_remote_assistance_intent:
            raise ValueError("can_show_remote_assistance_intent must be True")
        if not self.can_show_audit_state:
            raise ValueError("can_show_audit_state must be True")
        if self.dashboard_direct_execution_allowed:
            raise ValueError("dashboard_direct_execution_allowed must be False")
        if self.device_control_execution_allowed:
            raise ValueError("device_control_execution_allowed must be False")
        if self.child_control_allowed:
            raise ValueError("child_control_allowed must be False")
        if self.family_children_surface_allowed:
            raise ValueError("family_children_surface_allowed must be False for Phone Window")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    @classmethod
    def default(cls, *, panel_id: str) -> "PhoneScreenWindowPanelContract":
        return cls(
            panel_id=panel_id,
            panel_kind="phone_screen_window",
            dashboard_section="Phone Window",
            source_binding="mobile_screen_observer",
            read_model_binding="PhoneScreenWindowReadModel",
            read_only_default=True,
            can_show_frame_reference=True,
            can_show_consent_state=True,
            can_show_remote_assistance_intent=True,
            can_show_audit_state=True,
            dashboard_direct_execution_allowed=False,
            device_control_execution_allowed=False,
            child_control_allowed=False,
            family_children_surface_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "panel_id": self.panel_id,
            "panel_kind": self.panel_kind,
            "dashboard_section": self.dashboard_section,
            "source_binding": self.source_binding,
            "read_model_binding": self.read_model_binding,
            "read_only_default": self.read_only_default,
            "can_show_frame_reference": self.can_show_frame_reference,
            "can_show_consent_state": self.can_show_consent_state,
            "can_show_remote_assistance_intent": self.can_show_remote_assistance_intent,
            "can_show_audit_state": self.can_show_audit_state,
            "dashboard_direct_execution_allowed": self.dashboard_direct_execution_allowed,
            "device_control_execution_allowed": self.device_control_execution_allowed,
            "child_control_allowed": self.child_control_allowed,
            "family_children_surface_allowed": self.family_children_surface_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
