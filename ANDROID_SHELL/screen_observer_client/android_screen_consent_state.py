from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_CONSENT_STATES: tuple[str, ...] = (
    "consent_required",
    "consent_granted",
    "consent_revoked",
    "blocked",
)


@dataclass(frozen=True)
class AndroidScreenConsentState:
    device_id: str
    owner_identity_id: str
    session_id: str
    consent_state: str
    consent_required: bool
    owner_visible: bool
    audit_required: bool
    permission_prompt_allowed: bool
    android_platform_api_call_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("device_id", "owner_identity_id", "session_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.consent_state not in _ALLOWED_CONSENT_STATES:
            raise ValueError(f"unsupported consent_state: {self.consent_state}")

        if not self.consent_required:
            raise ValueError("consent_required must be True")
        if not self.owner_visible:
            raise ValueError("owner_visible must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if self.permission_prompt_allowed:
            raise ValueError("permission_prompt_allowed must be False in BATCH 4.4")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    def is_granted(self) -> bool:
        return self.consent_state == "consent_granted"

    def to_read_model(self) -> dict[str, object]:
        return {
            "device_id": self.device_id,
            "owner_identity_id": self.owner_identity_id,
            "session_id": self.session_id,
            "consent_state": self.consent_state,
            "consent_granted": self.is_granted(),
            "consent_required": self.consent_required,
            "owner_visible": self.owner_visible,
            "audit_required": self.audit_required,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
