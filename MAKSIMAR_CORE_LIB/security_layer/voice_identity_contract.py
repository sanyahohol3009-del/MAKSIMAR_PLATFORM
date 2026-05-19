from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VoiceIdentityStatus(str, Enum):
    VERIFIED = "verified"
    NOT_VERIFIED = "not_verified"
    MISSING_SAMPLE = "missing_sample"
    BELOW_THRESHOLD = "below_threshold"


@dataclass(frozen=True, slots=True)
class VoiceIdentityClaim:
    subject_id: str
    voiceprint_id: str
    confidence: float
    threshold: float
    sample_present: bool

    def __post_init__(self) -> None:
        if not self.subject_id:
            raise ValueError("subject_id must not be empty")
        if self.sample_present and not self.voiceprint_id:
            raise ValueError("voiceprint_id must be present when sample_present is true")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class VoiceIdentityVerification:
    subject_id: str
    status: VoiceIdentityStatus
    confidence: float
    threshold: float
    verified: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.subject_id:
            raise ValueError("subject_id must not be empty")
        if not isinstance(self.status, VoiceIdentityStatus):
            raise TypeError("status must be VoiceIdentityStatus")
        if self.verified and self.status is not VoiceIdentityStatus.VERIFIED:
            raise ValueError("verified requires VERIFIED status")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def verify_voice_identity(claim: VoiceIdentityClaim) -> VoiceIdentityVerification:
    if not claim.sample_present:
        return VoiceIdentityVerification(
            subject_id=claim.subject_id,
            status=VoiceIdentityStatus.MISSING_SAMPLE,
            confidence=claim.confidence,
            threshold=claim.threshold,
            verified=False,
            reason_codes=("voice_sample_missing",),
        )

    if claim.confidence < claim.threshold:
        return VoiceIdentityVerification(
            subject_id=claim.subject_id,
            status=VoiceIdentityStatus.BELOW_THRESHOLD,
            confidence=claim.confidence,
            threshold=claim.threshold,
            verified=False,
            reason_codes=("voice_confidence_below_threshold",),
        )

    return VoiceIdentityVerification(
        subject_id=claim.subject_id,
        status=VoiceIdentityStatus.VERIFIED,
        confidence=claim.confidence,
        threshold=claim.threshold,
        verified=True,
        reason_codes=("voice_identity_verified",),
    )
