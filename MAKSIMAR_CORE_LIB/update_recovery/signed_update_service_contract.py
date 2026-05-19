from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.update_signature_verifier_contract import (
    UpdateSignatureDecisionReadModel,
    UpdateSignatureDecisionStatus,
    UpdateSignatureVerificationRequest,
    verify_update_package_signature,
)


SIGNED_UPDATE_SERVICE_CONTRACT_ID = "signed_update_service_contract_v1"


class SignedUpdateServiceStatus(str, Enum):
    SIGNED_UPDATE_READY_FOR_POLICY = "signed_update_ready_for_policy"
    SIGNED_UPDATE_REJECTED_BY_SIGNATURE_GATE = "signed_update_rejected_by_signature_gate"


@dataclass(frozen=True, slots=True)
class SignedUpdateServiceRequest:
    service_request_id: str
    signature_verification_request: UpdateSignatureVerificationRequest
    dashboard_execution_allowed: bool = False
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("service_request_id", self.service_request_id)
        if not isinstance(self.signature_verification_request, UpdateSignatureVerificationRequest):
            raise TypeError("signature_verification_request must be UpdateSignatureVerificationRequest")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


@dataclass(frozen=True, slots=True)
class SignedUpdateServiceDecisionReadModel:
    service_decision_id: str
    contract_id: str
    service_request_id: str
    package_id: str
    service_status: SignedUpdateServiceStatus
    signature_decision: UpdateSignatureDecisionReadModel
    signed_update_accepted: bool
    update_package_apply_allowed: bool
    snapshot_required_before_apply: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("service_decision_id", self.service_decision_id)
        if self.contract_id != SIGNED_UPDATE_SERVICE_CONTRACT_ID:
            raise ValueError("contract_id must be signed_update_service_contract_v1")
        _validate_non_empty("service_request_id", self.service_request_id)
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.service_status, SignedUpdateServiceStatus):
            raise TypeError("service_status must be SignedUpdateServiceStatus")
        if not isinstance(self.signature_decision, UpdateSignatureDecisionReadModel):
            raise TypeError("signature_decision must be UpdateSignatureDecisionReadModel")
        if self.signed_update_accepted:
            if self.service_status is not SignedUpdateServiceStatus.SIGNED_UPDATE_READY_FOR_POLICY:
                raise ValueError("signed_update_accepted requires SIGNED_UPDATE_READY_FOR_POLICY")
            if self.signature_decision.status is not UpdateSignatureDecisionStatus.ACCEPTED:
                raise ValueError("signed_update_accepted requires accepted signature decision")
        if self.update_package_apply_allowed:
            raise ValueError("update_package_apply_allowed must remain false in BATCH 3.2")
        if not self.snapshot_required_before_apply:
            raise ValueError("snapshot_required_before_apply must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        _validate_string_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_decision_id": self.service_decision_id,
            "contract_id": self.contract_id,
            "service_request_id": self.service_request_id,
            "package_id": self.package_id,
            "service_status": self.service_status.value,
            "signature_decision": self.signature_decision.to_dict(),
            "signed_update_accepted": self.signed_update_accepted,
            "update_package_apply_allowed": self.update_package_apply_allowed,
            "snapshot_required_before_apply": self.snapshot_required_before_apply,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def evaluate_signed_update_service(
    request: SignedUpdateServiceRequest,
) -> SignedUpdateServiceDecisionReadModel:
    if not isinstance(request, SignedUpdateServiceRequest):
        raise TypeError("request must be SignedUpdateServiceRequest")

    signature_decision = verify_update_package_signature(request.signature_verification_request)
    accepted = signature_decision.status is UpdateSignatureDecisionStatus.ACCEPTED

    if accepted:
        return SignedUpdateServiceDecisionReadModel(
            service_decision_id=f"signed_update_service_decision:{request.service_request_id}",
            contract_id=SIGNED_UPDATE_SERVICE_CONTRACT_ID,
            service_request_id=request.service_request_id,
            package_id=signature_decision.package_id,
            service_status=SignedUpdateServiceStatus.SIGNED_UPDATE_READY_FOR_POLICY,
            signature_decision=signature_decision,
            signed_update_accepted=True,
            update_package_apply_allowed=False,
            snapshot_required_before_apply=True,
            reason_codes=("signed_update_verified_for_policy_gate", "snapshot_required_before_apply"),
        )

    return SignedUpdateServiceDecisionReadModel(
        service_decision_id=f"signed_update_service_decision:{request.service_request_id}",
        contract_id=SIGNED_UPDATE_SERVICE_CONTRACT_ID,
        service_request_id=request.service_request_id,
        package_id=signature_decision.package_id,
        service_status=SignedUpdateServiceStatus.SIGNED_UPDATE_REJECTED_BY_SIGNATURE_GATE,
        signature_decision=signature_decision,
        signed_update_accepted=False,
        update_package_apply_allowed=False,
        snapshot_required_before_apply=True,
        reason_codes=("signed_update_rejected_by_signature_gate",) + signature_decision.reason_codes,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_string_tuple(field_name: str, values: tuple[str, ...]) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not values:
        raise ValueError(f"{field_name} must not be empty")
    for value in values:
        _validate_non_empty(field_name, value)
