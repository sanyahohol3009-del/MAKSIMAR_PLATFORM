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
class AndroidTrainingSyncContract:
    contract_id: str
    platform: str
    training_sync_contract: bool
    training_sync_started: bool
    training_data_upload_allowed: bool
    raw_private_data_upload_allowed: bool
    canonical_memory_write_allowed: bool
    mobile_feedback_allowed: bool
    mobile_feedback_is_proposal_only: bool
    server_review_required: bool
    owner_approval_required: bool
    no_cross_owner_leak: bool
    no_cross_tenant_leak: bool
    server_remains_canonical_authority: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "platform", _ensure_non_empty(self.platform, "platform"))
        if self.platform != "android":
            raise ValueError("platform must be android")
        for field_name in (
            "training_sync_contract",
            "mobile_feedback_allowed",
            "mobile_feedback_is_proposal_only",
            "server_review_required",
            "owner_approval_required",
            "no_cross_owner_leak",
            "no_cross_tenant_leak",
            "server_remains_canonical_authority",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "training_sync_started",
            "training_data_upload_allowed",
            "raw_private_data_upload_allowed",
            "canonical_memory_write_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "platform": self.platform,
            "training_sync_contract": self.training_sync_contract,
            "training_sync_started": self.training_sync_started,
            "training_data_upload_allowed": self.training_data_upload_allowed,
            "raw_private_data_upload_allowed": self.raw_private_data_upload_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "mobile_feedback_allowed": self.mobile_feedback_allowed,
            "mobile_feedback_is_proposal_only": self.mobile_feedback_is_proposal_only,
            "server_review_required": self.server_review_required,
            "owner_approval_required": self.owner_approval_required,
            "no_cross_owner_leak": self.no_cross_owner_leak,
            "no_cross_tenant_leak": self.no_cross_tenant_leak,
            "server_remains_canonical_authority": self.server_remains_canonical_authority,
        }


def build_android_training_sync_contract() -> AndroidTrainingSyncContract:
    return AndroidTrainingSyncContract(
        contract_id="android_training_sync_contract_v0_1",
        platform="android",
        training_sync_contract=True,
        training_sync_started=False,
        training_data_upload_allowed=False,
        raw_private_data_upload_allowed=False,
        canonical_memory_write_allowed=False,
        mobile_feedback_allowed=True,
        mobile_feedback_is_proposal_only=True,
        server_review_required=True,
        owner_approval_required=True,
        no_cross_owner_leak=True,
        no_cross_tenant_leak=True,
        server_remains_canonical_authority=True,
    )
