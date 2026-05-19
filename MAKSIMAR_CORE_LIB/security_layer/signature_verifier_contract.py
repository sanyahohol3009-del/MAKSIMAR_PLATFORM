from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SignatureVerificationStatus(str, Enum):
    VALID = "valid"
    MISSING = "missing"
    INVALID = "invalid"
    UNSUPPORTED_ALGORITHM = "unsupported_algorithm"


@dataclass(frozen=True, slots=True)
class SignatureVerificationRequest:
    subject_id: str
    artifact_id: str
    payload_hash: str
    signature: str
    algorithm: str
    trust_domain: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("subject_id", self.subject_id),
            ("artifact_id", self.artifact_id),
            ("payload_hash", self.payload_hash),
            ("algorithm", self.algorithm),
            ("trust_domain", self.trust_domain),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")


@dataclass(frozen=True, slots=True)
class SignatureVerificationResult:
    status: SignatureVerificationStatus
    artifact_id: str
    reason_codes: tuple[str, ...]
    trust_boundary: str
    verified: bool
    dashboard_safe: bool = True
    update_package_specific: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.status, SignatureVerificationStatus):
            raise TypeError("status must be SignatureVerificationStatus")
        if not self.artifact_id:
            raise ValueError("artifact_id must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.trust_boundary:
            raise ValueError("trust_boundary must not be empty")
        if self.verified and self.status is not SignatureVerificationStatus.VALID:
            raise ValueError("verified requires VALID status")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.update_package_specific:
            raise ValueError("security signature verifier must remain generic, not update-package-specific")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def verify_generic_signature(
    request: SignatureVerificationRequest,
    *,
    trusted_signature: str,
    supported_algorithms: tuple[str, ...] = ("ed25519", "rsa_pss_sha256"),
) -> SignatureVerificationResult:
    if request.algorithm not in supported_algorithms:
        return SignatureVerificationResult(
            status=SignatureVerificationStatus.UNSUPPORTED_ALGORITHM,
            artifact_id=request.artifact_id,
            reason_codes=("unsupported_signature_algorithm",),
            trust_boundary=request.trust_domain,
            verified=False,
        )

    if not request.signature:
        return SignatureVerificationResult(
            status=SignatureVerificationStatus.MISSING,
            artifact_id=request.artifact_id,
            reason_codes=("signature_missing",),
            trust_boundary=request.trust_domain,
            verified=False,
        )

    if request.signature != trusted_signature:
        return SignatureVerificationResult(
            status=SignatureVerificationStatus.INVALID,
            artifact_id=request.artifact_id,
            reason_codes=("signature_invalid",),
            trust_boundary=request.trust_domain,
            verified=False,
        )

    return SignatureVerificationResult(
        status=SignatureVerificationStatus.VALID,
        artifact_id=request.artifact_id,
        reason_codes=("signature_valid",),
        trust_boundary=request.trust_domain,
        verified=True,
    )
