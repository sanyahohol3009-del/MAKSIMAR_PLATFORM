from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_CONSENT_STATES = ("not_requested", "requested", "granted", "revoked", "expired", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


@dataclass(frozen=True)
class MobileScreenConsentContract:
    """Explicit consent state for a mobile screen observer session."""

    consent_id: str
    session_id: str
    owner_identity_id: str
    device_id: str
    consent_state: str
    consent_epoch_ms: int
    expires_epoch_ms: int
    explicit_owner_consent_required: bool
    visible_on_device_required: bool
    audit_event_required: bool
    revocation_supported: bool
    remote_assistance_enabled_by_default: bool
    dashboard_bypass_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "consent_id", _ensure_non_empty(self.consent_id, "consent_id"))
        object.__setattr__(self, "session_id", _ensure_non_empty(self.session_id, "session_id"))
        object.__setattr__(
            self,
            "owner_identity_id",
            _ensure_non_empty(self.owner_identity_id, "owner_identity_id"),
        )
        object.__setattr__(self, "device_id", _ensure_non_empty(self.device_id, "device_id"))

        if self.consent_state not in _ALLOWED_CONSENT_STATES:
            raise ValueError(f"consent_state must be one of {_ALLOWED_CONSENT_STATES}: {self.consent_state}")

        object.__setattr__(
            self,
            "consent_epoch_ms",
            _ensure_non_negative_int(self.consent_epoch_ms, "consent_epoch_ms"),
        )
        object.__setattr__(
            self,
            "expires_epoch_ms",
            _ensure_non_negative_int(self.expires_epoch_ms, "expires_epoch_ms"),
        )

        if self.consent_state == "granted" and self.expires_epoch_ms <= self.consent_epoch_ms:
            raise ValueError("granted consent must expire after consent_epoch_ms")
        if not self.explicit_owner_consent_required:
            raise ValueError("explicit_owner_consent_required must be True")
        if not self.visible_on_device_required:
            raise ValueError("visible_on_device_required must be True")
        if not self.audit_event_required:
            raise ValueError("audit_event_required must be True")
        if not self.revocation_supported:
            raise ValueError("revocation_supported must be True")
        if self.remote_assistance_enabled_by_default:
            raise ValueError("remote_assistance_enabled_by_default must be False")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
