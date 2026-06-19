from __future__ import annotations

import getpass
import os
from dataclasses import dataclass
from typing import Any


_ALLOWED_SOURCES = {
    "local_terminal_session",
    "voice_unverified",
}


@dataclass(frozen=True, slots=True)
class OwnerIdentityClaim:
    claim_id: str
    source: str
    verified: bool
    verification_method: str
    session_token_present: bool
    process_owner_matches_os_user: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.claim_id, "claim_id")
        _require_non_empty(self.source, "source")
        _require_non_empty(self.verification_method, "verification_method")
        if self.source not in _ALLOWED_SOURCES:
            raise ValueError(f"unsupported owner identity source: {self.source!r}")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.source == "voice_unverified" and self.verified:
            raise ValueError("voice_unverified must never be verified")
        if self.verified and self.source != "local_terminal_session":
            raise ValueError("only local_terminal_session may verify direct owner identity in v1")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "source": self.source,
            "verified": self.verified,
            "verification_method": self.verification_method,
            "session_token_present": self.session_token_present,
            "process_owner_matches_os_user": self.process_owner_matches_os_user,
            "reason_codes": self.reason_codes,
        }


def build_owner_identity_claim_for_terminal() -> OwnerIdentityClaim:
    os_user = getpass.getuser()
    owner_os_user = os.environ.get("JARVIS_OWNER_OS_USER", "aleksandr").strip() or "aleksandr"
    matches = os_user == owner_os_user
    return OwnerIdentityClaim(
        claim_id="terminal_session_claim_v1",
        source="local_terminal_session",
        verified=matches,
        verification_method="os_user_match",
        session_token_present=False,
        process_owner_matches_os_user=matches,
        reason_codes=("os_user_verified",) if matches else ("os_user_mismatch",),
    )


def build_owner_identity_claim_for_voice_unverified() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="voice_unverified_claim_v1",
        source="voice_unverified",
        verified=False,
        verification_method="none_voice_biometric_not_implemented",
        session_token_present=False,
        process_owner_matches_os_user=False,
        reason_codes=(
            "voice_biometric_not_implemented",
            "voice_cannot_authorize_direct_action",
        ),
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
