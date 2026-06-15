from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class MirrorDriftDetectionContract:
    contract_id: str
    mirror_drift_detection_enabled: bool
    detects_mobile_mirror_drift: bool
    drift_detection_read_only: bool
    drift_report_is_evidence_only: bool
    auto_resolution_allowed: bool
    mobile_side_canonical_update_allowed: bool
    junior_model_can_resolve_drift: bool
    server_review_required: bool
    server_remains_canonical_authority: bool
    no_cross_owner_leak: bool
    no_cross_tenant_leak: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        _require_true(
            self.mirror_drift_detection_enabled,
            "mirror_drift_detection_enabled",
        )
        _require_true(
            self.detects_mobile_mirror_drift,
            "detects_mobile_mirror_drift",
        )
        _require_true(self.drift_detection_read_only, "drift_detection_read_only")
        _require_true(
            self.drift_report_is_evidence_only,
            "drift_report_is_evidence_only",
        )
        _require_false(self.auto_resolution_allowed, "auto_resolution_allowed")
        _require_false(
            self.mobile_side_canonical_update_allowed,
            "mobile_side_canonical_update_allowed",
        )
        _require_false(
            self.junior_model_can_resolve_drift,
            "junior_model_can_resolve_drift",
        )
        _require_true(self.server_review_required, "server_review_required")
        _require_true(
            self.server_remains_canonical_authority,
            "server_remains_canonical_authority",
        )
        _require_true(self.no_cross_owner_leak, "no_cross_owner_leak")
        _require_true(self.no_cross_tenant_leak, "no_cross_tenant_leak")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_true(self.proposal_only, "proposal_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "mirror_drift_detection_enabled": self.mirror_drift_detection_enabled,
            "detects_mobile_mirror_drift": self.detects_mobile_mirror_drift,
            "drift_detection_read_only": self.drift_detection_read_only,
            "drift_report_is_evidence_only": self.drift_report_is_evidence_only,
            "auto_resolution_allowed": self.auto_resolution_allowed,
            "mobile_side_canonical_update_allowed": (
                self.mobile_side_canonical_update_allowed
            ),
            "junior_model_can_resolve_drift": self.junior_model_can_resolve_drift,
            "server_review_required": self.server_review_required,
            "server_remains_canonical_authority": (
                self.server_remains_canonical_authority
            ),
            "no_cross_owner_leak": self.no_cross_owner_leak,
            "no_cross_tenant_leak": self.no_cross_tenant_leak,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "proposal_only": self.proposal_only,
        }


def build_mirror_drift_detection_contract() -> MirrorDriftDetectionContract:
    return MirrorDriftDetectionContract(
        contract_id="mirror_drift_detection_contract_v0_1",
        mirror_drift_detection_enabled=True,
        detects_mobile_mirror_drift=True,
        drift_detection_read_only=True,
        drift_report_is_evidence_only=True,
        auto_resolution_allowed=False,
        mobile_side_canonical_update_allowed=False,
        junior_model_can_resolve_drift=False,
        server_review_required=True,
        server_remains_canonical_authority=True,
        no_cross_owner_leak=True,
        no_cross_tenant_leak=True,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        proposal_only=True,
    )
