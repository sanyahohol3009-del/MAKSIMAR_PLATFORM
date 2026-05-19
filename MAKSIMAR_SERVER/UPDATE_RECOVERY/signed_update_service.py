from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.signed_update_service_contract import (
    SignedUpdateServiceDecisionReadModel,
    SignedUpdateServiceRequest,
    evaluate_signed_update_service,
)


SIGNED_UPDATE_SERVICE_RUNTIME_ID = "signed_update_service_runtime_v1"


@dataclass(frozen=True, slots=True)
class SignedUpdateServiceRuntimeResult:
    runtime_id: str
    service_request_id: str
    decision: SignedUpdateServiceDecisionReadModel
    wrapper_only: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.runtime_id != SIGNED_UPDATE_SERVICE_RUNTIME_ID:
            raise ValueError("runtime_id must be signed_update_service_runtime_v1")
        _validate_non_empty("service_request_id", self.service_request_id)
        if not isinstance(self.decision, SignedUpdateServiceDecisionReadModel):
            raise TypeError("decision must be SignedUpdateServiceDecisionReadModel")
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
            "service_request_id": self.service_request_id,
            "decision": self.decision.to_dict(),
            "wrapper_only": self.wrapper_only,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "reason_codes": self.reason_codes,
        }


def run_signed_update_service(
    request: SignedUpdateServiceRequest,
) -> SignedUpdateServiceRuntimeResult:
    if not isinstance(request, SignedUpdateServiceRequest):
        raise TypeError("request must be SignedUpdateServiceRequest")

    decision = evaluate_signed_update_service(request)
    return SignedUpdateServiceRuntimeResult(
        runtime_id=SIGNED_UPDATE_SERVICE_RUNTIME_ID,
        service_request_id=request.service_request_id,
        decision=decision,
        wrapper_only=True,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=("signed_update_service_runtime_wrapped_contract",),
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
