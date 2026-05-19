from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from MAKSIMAR_CORE_LIB.security_layer.signature_verifier_contract import (
    SignatureVerificationResult,
    SignatureVerificationStatus,
)


class ExecutionBundleVerificationStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ExecutionBundle:
    bundle_id: str
    request_id: str
    trace_id: str
    command_kind: str
    target_layer_id: str
    signature_result: SignatureVerificationResult
    approval_present: bool
    voice_identity_verified: bool
    high_risk: bool

    def __post_init__(self) -> None:
        for field_name, value in (
            ("bundle_id", self.bundle_id),
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("command_kind", self.command_kind),
            ("target_layer_id", self.target_layer_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.signature_result, SignatureVerificationResult):
            raise TypeError("signature_result must be SignatureVerificationResult")


@dataclass(frozen=True, slots=True)
class ExecutionBundleVerificationResult:
    bundle_id: str
    status: ExecutionBundleVerificationStatus
    ready_for_execution: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.bundle_id:
            raise ValueError("bundle_id must not be empty")
        if not isinstance(self.status, ExecutionBundleVerificationStatus):
            raise TypeError("status must be ExecutionBundleVerificationStatus")
        if self.ready_for_execution and self.status is not ExecutionBundleVerificationStatus.READY:
            raise ValueError("ready_for_execution requires READY status")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def verify_execution_bundle(bundle: ExecutionBundle) -> ExecutionBundleVerificationResult:
    reasons: list[str] = []

    if bundle.signature_result.status is not SignatureVerificationStatus.VALID:
        reasons.append("signature_not_valid")

    if bundle.high_risk and not bundle.approval_present:
        reasons.append("approval_missing_for_high_risk")

    if bundle.high_risk and not bundle.voice_identity_verified:
        reasons.append("voice_identity_missing_for_high_risk")

    if reasons:
        return ExecutionBundleVerificationResult(
            bundle_id=bundle.bundle_id,
            status=ExecutionBundleVerificationStatus.BLOCKED,
            ready_for_execution=False,
            reason_codes=tuple(reasons),
        )

    return ExecutionBundleVerificationResult(
        bundle_id=bundle.bundle_id,
        status=ExecutionBundleVerificationStatus.READY,
        ready_for_execution=True,
        reason_codes=("execution_bundle_ready",),
    )
