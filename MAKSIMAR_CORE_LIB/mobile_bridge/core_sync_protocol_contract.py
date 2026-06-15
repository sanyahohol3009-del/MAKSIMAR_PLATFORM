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
class CoreSyncProtocolContract:
    contract_id: str
    sync_direction: str
    mobile_feedback_allowed: bool
    mobile_feedback_is_proposal_only: bool
    mobile_feedback_canonical_write: bool
    junior_sync_authority: bool
    server_remains_canonical_authority: bool
    conflict_resolution_on_server_only: bool
    offline_cache_allowed: bool
    offline_cache_canonical: bool
    no_cross_owner_leak: bool
    no_cross_tenant_leak: bool
    approval_required_for_mutation: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "sync_direction", _ensure_non_empty(self.sync_direction, "sync_direction"))
        if self.sync_direction != "server_senior_to_mobile_junior":
            raise ValueError("sync_direction must be server_senior_to_mobile_junior")
        _require_true(self.mobile_feedback_allowed, "mobile_feedback_allowed")
        _require_true(
            self.mobile_feedback_is_proposal_only,
            "mobile_feedback_is_proposal_only",
        )
        _require_false(
            self.mobile_feedback_canonical_write,
            "mobile_feedback_canonical_write",
        )
        _require_false(self.junior_sync_authority, "junior_sync_authority")
        _require_true(
            self.server_remains_canonical_authority,
            "server_remains_canonical_authority",
        )
        _require_true(
            self.conflict_resolution_on_server_only,
            "conflict_resolution_on_server_only",
        )
        _require_true(self.offline_cache_allowed, "offline_cache_allowed")
        _require_false(self.offline_cache_canonical, "offline_cache_canonical")
        _require_true(self.no_cross_owner_leak, "no_cross_owner_leak")
        _require_true(self.no_cross_tenant_leak, "no_cross_tenant_leak")
        _require_true(
            self.approval_required_for_mutation,
            "approval_required_for_mutation",
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "sync_direction": self.sync_direction,
            "mobile_feedback_allowed": self.mobile_feedback_allowed,
            "mobile_feedback_is_proposal_only": self.mobile_feedback_is_proposal_only,
            "mobile_feedback_canonical_write": self.mobile_feedback_canonical_write,
            "junior_sync_authority": self.junior_sync_authority,
            "server_remains_canonical_authority": self.server_remains_canonical_authority,
            "conflict_resolution_on_server_only": self.conflict_resolution_on_server_only,
            "offline_cache_allowed": self.offline_cache_allowed,
            "offline_cache_canonical": self.offline_cache_canonical,
            "no_cross_owner_leak": self.no_cross_owner_leak,
            "no_cross_tenant_leak": self.no_cross_tenant_leak,
            "approval_required_for_mutation": self.approval_required_for_mutation,
        }


def build_core_sync_protocol_contract() -> CoreSyncProtocolContract:
    return CoreSyncProtocolContract(
        contract_id="core_sync_protocol_contract_v0_1",
        sync_direction="server_senior_to_mobile_junior",
        mobile_feedback_allowed=True,
        mobile_feedback_is_proposal_only=True,
        mobile_feedback_canonical_write=False,
        junior_sync_authority=False,
        server_remains_canonical_authority=True,
        conflict_resolution_on_server_only=True,
        offline_cache_allowed=True,
        offline_cache_canonical=False,
        no_cross_owner_leak=True,
        no_cross_tenant_leak=True,
        approval_required_for_mutation=True,
    )
