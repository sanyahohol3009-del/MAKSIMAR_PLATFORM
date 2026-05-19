from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.update_signature_verifier_contract import (
    UpdateSignatureDecisionReadModel,
    UpdateSignatureVerificationRequest,
    verify_update_package_signature,
)


UPDATE_SIGNATURE_VERIFIER_RUNTIME_ID = "update_signature_verifier_runtime_v1"


@dataclass(frozen=True, slots=True)
class UpdateSignatureVerifierRuntimeResult:
    runtime_id: str
    request_id: str
    decision: UpdateSignatureDecisionReadModel
    wrapper_only: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.runtime_id != UPDATE_SIGNATURE_VERIFIER_RUNTIME_ID:
            raise ValueError("runtime_id must be update_signature_verifier_runtime_v1")
        _validate_non_empty("request_id", self.request_id)
        if not isinstance(self.decision, UpdateSignatureDecisionReadModel):
            raise TypeError("decision must be UpdateSignatureDecisionReadModel")
        if not self.wrapper_only:
            raise ValueError("wrapper_only must remain true")
        _validate_runtime_safety_flags(
            runtime_apply_allowed=self.runtime_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_id": self.runtime_id,
            "request_id": self.request_id,
            "decision": self.decision.to_dict(),
            "wrapper_only": self.wrapper_only,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "reason_codes": self.reason_codes,
        }


def run_update_signature_verifier(
    request: UpdateSignatureVerificationRequest,
) -> UpdateSignatureVerifierRuntimeResult:
    if not isinstance(request, UpdateSignatureVerificationRequest):
        raise TypeError("request must be UpdateSignatureVerificationRequest")

    decision = verify_update_package_signature(request)
    return UpdateSignatureVerifierRuntimeResult(
        runtime_id=UPDATE_SIGNATURE_VERIFIER_RUNTIME_ID,
        request_id=request.request_id,
        decision=decision,
        wrapper_only=True,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=("update_signature_verifier_runtime_wrapped_contract",),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


def _validate_runtime_safety_flags(
    *,
    runtime_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if runtime_apply_allowed:
        raise ValueError("runtime_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
