from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_BUTTON_IDS: tuple[str, ...] = (
    "refresh_frame_reference",
    "request_remote_assistance",
    "revoke_screen_consent",
    "open_family_children_section",
)
_ALLOWED_INTENT_TYPES: tuple[str, ...] = (
    "read_model_refresh",
    "remote_assistance_request",
    "consent_revoke_request",
    "navigation_request",
)


@dataclass(frozen=True)
class PhoneScreenButtonIntentContract:
    intent_id: str
    panel_id: str
    device_id: str
    owner_identity_id: str
    button_id: str
    intent_type: str
    approval_required: bool
    audit_required: bool
    read_only_intent: bool
    dashboard_direct_execution_allowed: bool
    device_control_execution_allowed: bool
    remote_assistance_requires_approval: bool
    child_control_intent_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("intent_id", "panel_id", "device_id", "owner_identity_id", "button_id", "intent_type"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.button_id not in _ALLOWED_BUTTON_IDS:
            raise ValueError(f"unsupported button_id: {self.button_id}")
        if self.intent_type not in _ALLOWED_INTENT_TYPES:
            raise ValueError(f"unsupported intent_type: {self.intent_type}")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.read_only_intent:
            raise ValueError("read_only_intent must be True")
        if self.dashboard_direct_execution_allowed:
            raise ValueError("dashboard_direct_execution_allowed must be False")
        if self.device_control_execution_allowed:
            raise ValueError("device_control_execution_allowed must be False")
        if not self.remote_assistance_requires_approval:
            raise ValueError("remote_assistance_requires_approval must be True")
        if self.child_control_intent_allowed:
            raise ValueError("child_control_intent_allowed must be False for Phone Window")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    @classmethod
    def remote_assistance_request(
        cls,
        *,
        intent_id: str,
        panel_id: str,
        device_id: str,
        owner_identity_id: str,
    ) -> "PhoneScreenButtonIntentContract":
        return cls(
            intent_id=intent_id,
            panel_id=panel_id,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            button_id="request_remote_assistance",
            intent_type="remote_assistance_request",
            approval_required=True,
            audit_required=True,
            read_only_intent=True,
            dashboard_direct_execution_allowed=False,
            device_control_execution_allowed=False,
            remote_assistance_requires_approval=True,
            child_control_intent_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "intent_id": self.intent_id,
            "panel_id": self.panel_id,
            "device_id": self.device_id,
            "owner_identity_id": self.owner_identity_id,
            "button_id": self.button_id,
            "intent_type": self.intent_type,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "read_only_intent": self.read_only_intent,
            "dashboard_direct_execution_allowed": self.dashboard_direct_execution_allowed,
            "device_control_execution_allowed": self.device_control_execution_allowed,
            "remote_assistance_requires_approval": self.remote_assistance_requires_approval,
            "child_control_intent_allowed": self.child_control_intent_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
