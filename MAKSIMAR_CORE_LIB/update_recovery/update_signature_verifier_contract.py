from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.update_package_models import (
    UpdatePackageManifest,
    UpdatePackageSignatureAlgorithm,
)


UPDATE_SIGNATURE_VERIFIER_CONTRACT_ID = "update_signature_verifier_contract_v1"


class UpdateSignatureDecisionStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class UpdateSignatureVerificationRequest:
    request_id: str
    package_manifest: UpdatePackageManifest
    trusted_signer_ids: tuple[str, ...]
    allowed_algorithms: tuple[UpdatePackageSignatureAlgorithm, ...]
    required_target_layer_ids: tuple[str, ...]
    dashboard_execution_allowed: bool = False
    direct_apply_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("request_id", self.request_id)
        if not isinstance(self.package_manifest, UpdatePackageManifest):
            raise TypeError("package_manifest must be UpdatePackageManifest")
        _validate_string_tuple("trusted_signer_ids", self.trusted_signer_ids)
        if not isinstance(self.allowed_algorithms, tuple):
            raise TypeError("allowed_algorithms must be a tuple")
        if not self.allowed_algorithms:
            raise ValueError("allowed_algorithms must not be empty")
        for algorithm in self.allowed_algorithms:
            if not isinstance(algorithm, UpdatePackageSignatureAlgorithm):
                raise TypeError("allowed_algorithms must contain UpdatePackageSignatureAlgorithm")
        _validate_string_tuple("required_target_layer_ids", self.required_target_layer_ids)
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")


@dataclass(frozen=True, slots=True)
class UpdateSignatureDecisionReadModel:
    decision_id: str
    contract_id: str
    request_id: str
    package_id: str
    status: UpdateSignatureDecisionStatus
    signature_verified: bool
    unsigned_update_rejected: bool
    signer_trusted: bool
    algorithm_allowed: bool
    target_layer_allowed: bool
    package_hash_valid: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("decision_id", self.decision_id)
        if self.contract_id != UPDATE_SIGNATURE_VERIFIER_CONTRACT_ID:
            raise ValueError("contract_id must be update_signature_verifier_contract_v1")
        _validate_non_empty("request_id", self.request_id)
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, UpdateSignatureDecisionStatus):
            raise TypeError("status must be UpdateSignatureDecisionStatus")

        if self.status is UpdateSignatureDecisionStatus.ACCEPTED:
            if not self.signature_verified:
                raise ValueError("accepted update signature decision requires signature_verified true")
            if self.unsigned_update_rejected:
                raise ValueError("accepted update signature decision cannot mark unsigned_update_rejected true")
            if not self.signer_trusted:
                raise ValueError("accepted update signature decision requires signer_trusted true")
            if not self.algorithm_allowed:
                raise ValueError("accepted update signature decision requires algorithm_allowed true")
            if not self.target_layer_allowed:
                raise ValueError("accepted update signature decision requires target_layer_allowed true")
            if not self.package_hash_valid:
                raise ValueError("accepted update signature decision requires package_hash_valid true")

        if self.status is UpdateSignatureDecisionStatus.REJECTED and self.signature_verified:
            raise ValueError("rejected update signature decision cannot have signature_verified true")
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
            "decision_id": self.decision_id,
            "contract_id": self.contract_id,
            "request_id": self.request_id,
            "package_id": self.package_id,
            "status": self.status.value,
            "signature_verified": self.signature_verified,
            "unsigned_update_rejected": self.unsigned_update_rejected,
            "signer_trusted": self.signer_trusted,
            "algorithm_allowed": self.algorithm_allowed,
            "target_layer_allowed": self.target_layer_allowed,
            "package_hash_valid": self.package_hash_valid,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def verify_update_package_signature(
    request: UpdateSignatureVerificationRequest,
) -> UpdateSignatureDecisionReadModel:
    if not isinstance(request, UpdateSignatureVerificationRequest):
        raise TypeError("request must be UpdateSignatureVerificationRequest")

    manifest = request.package_manifest
    signature = manifest.signature

    if signature is None:
        return _build_decision(
            request=request,
            status=UpdateSignatureDecisionStatus.REJECTED,
            signature_verified=False,
            unsigned_update_rejected=True,
            signer_trusted=False,
            algorithm_allowed=False,
            target_layer_allowed=manifest.target_layer_id in request.required_target_layer_ids,
            package_hash_valid=True,
            reason_codes=("unsigned_update_rejected", "update_signature_required"),
        )

    signer_trusted = signature.signer_id in request.trusted_signer_ids
    algorithm_allowed = signature.algorithm in request.allowed_algorithms
    target_layer_allowed = manifest.target_layer_id in request.required_target_layer_ids
    package_hash_valid = signature.signed_payload_sha256 == manifest.package_sha256

    accepted = signer_trusted and algorithm_allowed and target_layer_allowed and package_hash_valid

    if accepted:
        return _build_decision(
            request=request,
            status=UpdateSignatureDecisionStatus.ACCEPTED,
            signature_verified=True,
            unsigned_update_rejected=False,
            signer_trusted=True,
            algorithm_allowed=True,
            target_layer_allowed=True,
            package_hash_valid=True,
            reason_codes=("update_signature_verified", "trusted_update_signer", "target_layer_allowed"),
        )

    reason_codes: list[str] = ["update_signature_rejected"]
    if not signer_trusted:
        reason_codes.append("untrusted_update_signer")
    if not algorithm_allowed:
        reason_codes.append("unsupported_update_signature_algorithm")
    if not target_layer_allowed:
        reason_codes.append("target_layer_not_allowed")
    if not package_hash_valid:
        reason_codes.append("signed_payload_hash_mismatch")

    return _build_decision(
        request=request,
        status=UpdateSignatureDecisionStatus.REJECTED,
        signature_verified=False,
        unsigned_update_rejected=False,
        signer_trusted=signer_trusted,
        algorithm_allowed=algorithm_allowed,
        target_layer_allowed=target_layer_allowed,
        package_hash_valid=package_hash_valid,
        reason_codes=tuple(reason_codes),
    )


def _build_decision(
    *,
    request: UpdateSignatureVerificationRequest,
    status: UpdateSignatureDecisionStatus,
    signature_verified: bool,
    unsigned_update_rejected: bool,
    signer_trusted: bool,
    algorithm_allowed: bool,
    target_layer_allowed: bool,
    package_hash_valid: bool,
    reason_codes: tuple[str, ...],
) -> UpdateSignatureDecisionReadModel:
    return UpdateSignatureDecisionReadModel(
        decision_id=f"update_signature_decision:{request.request_id}",
        contract_id=UPDATE_SIGNATURE_VERIFIER_CONTRACT_ID,
        request_id=request.request_id,
        package_id=request.package_manifest.package_id,
        status=status,
        signature_verified=signature_verified,
        unsigned_update_rejected=unsigned_update_rejected,
        signer_trusted=signer_trusted,
        algorithm_allowed=algorithm_allowed,
        target_layer_allowed=target_layer_allowed,
        package_hash_valid=package_hash_valid,
        reason_codes=reason_codes,
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
