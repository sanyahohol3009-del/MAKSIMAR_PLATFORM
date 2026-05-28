from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardianAuthorityContract:
    guardian_id: str
    child_profile_id: str
    guardian_authority_verified: bool
    authority_scope: str
    audit_required: bool
    expires_epoch_ms: int

    def __post_init__(self) -> None:
        if not self.guardian_id.strip():
            raise ValueError("guardian_id must be non-empty")
        if not self.child_profile_id.strip():
            raise ValueError("child_profile_id must be non-empty")
        if not self.guardian_authority_verified:
            raise ValueError("guardian_authority_verified must be True")
        if self.authority_scope != "family_child_device_control":
            raise ValueError("authority_scope must be family_child_device_control")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not isinstance(self.expires_epoch_ms, int) or self.expires_epoch_ms <= 0:
            raise ValueError("expires_epoch_ms must be a positive integer")

    def can_authorize_child_control(self) -> bool:
        return True
