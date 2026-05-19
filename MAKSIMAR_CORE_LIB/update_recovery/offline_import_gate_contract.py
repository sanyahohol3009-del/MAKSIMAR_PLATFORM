from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


OFFLINE_IMPORT_GATE_CONTRACT_ID = "offline_import_gate_contract_v1"


class OfflineImportGateDecisionStatus(str, Enum):
    ACCEPTED_FOR_VERIFICATION = "accepted_for_verification"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class OfflineImportCandidate:
    import_id: str
    package_id: str
    source_uri: str
    package_sha256: str
    created_at_utc: str
    signature_present: bool
    air_gap_transfer_confirmed: bool
    media_quarantined: bool
    operator_approval_present: bool

    def __post_init__(self) -> None:
        _validate_non_empty("import_id", self.import_id)
        _validate_non_empty("package_id", self.package_id)
        _validate_non_empty("source_uri", self.source_uri)
        _validate_sha256("package_sha256", self.package_sha256)
        _validate_utc_timestamp("created_at_utc", self.created_at_utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "import_id": self.import_id,
            "package_id": self.package_id,
            "source_uri": self.source_uri,
            "package_sha256": self.package_sha256,
            "created_at_utc": self.created_at_utc,
            "signature_present": self.signature_present,
            "air_gap_transfer_confirmed": self.air_gap_transfer_confirmed,
            "media_quarantined": self.media_quarantined,
            "operator_approval_present": self.operator_approval_present,
        }


@dataclass(frozen=True, slots=True)
class OfflineImportGateDecisionReadModel:
    decision_id: str
    contract_id: str
    import_id: str
    package_id: str
    status: OfflineImportGateDecisionStatus
    signature_present: bool
    air_gap_transfer_confirmed: bool
    media_quarantined: bool
    operator_approval_present: bool
    offline_import_allowed_for_verification: bool
    update_apply_allowed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("decision_id", self.decision_id)
        if self.contract_id != OFFLINE_IMPORT_GATE_CONTRACT_ID:
            raise ValueError("contract_id must be offline_import_gate_contract_v1")
        _validate_non_empty("import_id", self.import_id)
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, OfflineImportGateDecisionStatus):
            raise TypeError("status must be OfflineImportGateDecisionStatus")

        if self.status is OfflineImportGateDecisionStatus.ACCEPTED_FOR_VERIFICATION:
            if not self.signature_present:
                raise ValueError("accepted offline import requires signature_present true")
            if not self.air_gap_transfer_confirmed:
                raise ValueError("accepted offline import requires air_gap_transfer_confirmed true")
            if not self.media_quarantined:
                raise ValueError("accepted offline import requires media_quarantined true")
            if not self.operator_approval_present:
                raise ValueError("accepted offline import requires operator_approval_present true")
            if not self.offline_import_allowed_for_verification:
                raise ValueError("accepted offline import requires offline_import_allowed_for_verification true")

        if self.status is OfflineImportGateDecisionStatus.REJECTED and self.offline_import_allowed_for_verification:
            raise ValueError("rejected offline import cannot be allowed for verification")
        if self.update_apply_allowed:
            raise ValueError("update_apply_allowed must remain false")
        _validate_reason_codes(self.reason_codes)
        _validate_safety_flags(
            dashboard_safe=self.dashboard_safe,
            direct_apply_allowed=self.direct_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "contract_id": self.contract_id,
            "import_id": self.import_id,
            "package_id": self.package_id,
            "status": self.status.value,
            "signature_present": self.signature_present,
            "air_gap_transfer_confirmed": self.air_gap_transfer_confirmed,
            "media_quarantined": self.media_quarantined,
            "operator_approval_present": self.operator_approval_present,
            "offline_import_allowed_for_verification": self.offline_import_allowed_for_verification,
            "update_apply_allowed": self.update_apply_allowed,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def evaluate_offline_import_gate(
    candidate: OfflineImportCandidate,
) -> OfflineImportGateDecisionReadModel:
    if not isinstance(candidate, OfflineImportCandidate):
        raise TypeError("candidate must be OfflineImportCandidate")

    accepted = (
        candidate.signature_present
        and candidate.air_gap_transfer_confirmed
        and candidate.media_quarantined
        and candidate.operator_approval_present
    )

    if accepted:
        return OfflineImportGateDecisionReadModel(
            decision_id=f"offline_import_gate_decision:{candidate.import_id}",
            contract_id=OFFLINE_IMPORT_GATE_CONTRACT_ID,
            import_id=candidate.import_id,
            package_id=candidate.package_id,
            status=OfflineImportGateDecisionStatus.ACCEPTED_FOR_VERIFICATION,
            signature_present=True,
            air_gap_transfer_confirmed=True,
            media_quarantined=True,
            operator_approval_present=True,
            offline_import_allowed_for_verification=True,
            update_apply_allowed=False,
            reason_codes=("offline_import_quarantined", "signature_present", "operator_approved_for_verification"),
        )

    reason_codes: list[str] = ["offline_import_rejected"]
    if not candidate.signature_present:
        reason_codes.append("missing_signature")
    if not candidate.air_gap_transfer_confirmed:
        reason_codes.append("air_gap_transfer_not_confirmed")
    if not candidate.media_quarantined:
        reason_codes.append("media_quarantine_missing")
    if not candidate.operator_approval_present:
        reason_codes.append("operator_approval_missing")

    return OfflineImportGateDecisionReadModel(
        decision_id=f"offline_import_gate_decision:{candidate.import_id}",
        contract_id=OFFLINE_IMPORT_GATE_CONTRACT_ID,
        import_id=candidate.import_id,
        package_id=candidate.package_id,
        status=OfflineImportGateDecisionStatus.REJECTED,
        signature_present=candidate.signature_present,
        air_gap_transfer_confirmed=candidate.air_gap_transfer_confirmed,
        media_quarantined=candidate.media_quarantined,
        operator_approval_present=candidate.operator_approval_present,
        offline_import_allowed_for_verification=False,
        update_apply_allowed=False,
        reason_codes=tuple(reason_codes),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_sha256(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
    int(value, 16)


def _validate_utc_timestamp(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if "T" not in value or not value.endswith("Z"):
        raise ValueError(f"{field_name} must be an ISO-like UTC timestamp ending with Z")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


def _validate_safety_flags(
    *,
    dashboard_safe: bool,
    direct_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if not dashboard_safe:
        raise ValueError("dashboard_safe must remain true")
    if direct_apply_allowed:
        raise ValueError("direct_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
