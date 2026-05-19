from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.signed_update_service_contract import (
    SignedUpdateServiceDecisionReadModel,
)


UPDATE_RECOVERY_POLICY_ID = "update_recovery_policy_v1"


@dataclass(frozen=True, slots=True)
class UpdateRecoveryPolicy:
    policy_id: str
    update_signature_required: bool
    unsigned_update_allowed: bool
    snapshot_required_before_apply: bool
    direct_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    security_layer_signature_replacement_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.policy_id != UPDATE_RECOVERY_POLICY_ID:
            raise ValueError("policy_id must be update_recovery_policy_v1")
        if not self.update_signature_required:
            raise ValueError("update_signature_required must remain true")
        if self.unsigned_update_allowed:
            raise ValueError("unsigned_update_allowed must remain false")
        if not self.snapshot_required_before_apply:
            raise ValueError("snapshot_required_before_apply must remain true")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if self.security_layer_signature_replacement_allowed:
            raise ValueError("security_layer_signature_replacement_allowed must remain false")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "update_signature_required": self.update_signature_required,
            "unsigned_update_allowed": self.unsigned_update_allowed,
            "snapshot_required_before_apply": self.snapshot_required_before_apply,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "security_layer_signature_replacement_allowed": self.security_layer_signature_replacement_allowed,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class UpdateRecoveryPolicyDecisionReadModel:
    policy_decision_id: str
    policy_id: str
    package_id: str
    signed_update_service_decision: SignedUpdateServiceDecisionReadModel
    policy_accepted_for_next_gate: bool
    update_signature_required: bool
    unsigned_update_allowed: bool
    snapshot_required_before_apply: bool
    update_package_apply_allowed: bool
    security_layer_signature_replacement_allowed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.policy_decision_id:
            raise ValueError("policy_decision_id must not be empty")
        if self.policy_id != UPDATE_RECOVERY_POLICY_ID:
            raise ValueError("policy_id must be update_recovery_policy_v1")
        if not self.package_id:
            raise ValueError("package_id must not be empty")
        if not isinstance(self.signed_update_service_decision, SignedUpdateServiceDecisionReadModel):
            raise TypeError("signed_update_service_decision must be SignedUpdateServiceDecisionReadModel")
        if self.policy_accepted_for_next_gate and not self.signed_update_service_decision.signed_update_accepted:
            raise ValueError("policy_accepted_for_next_gate requires signed_update_accepted true")
        if not self.update_signature_required:
            raise ValueError("update_signature_required must remain true")
        if self.unsigned_update_allowed:
            raise ValueError("unsigned_update_allowed must remain false")
        if not self.snapshot_required_before_apply:
            raise ValueError("snapshot_required_before_apply must remain true")
        if self.update_package_apply_allowed:
            raise ValueError("update_package_apply_allowed must remain false in BATCH 3.2")
        if self.security_layer_signature_replacement_allowed:
            raise ValueError("security_layer_signature_replacement_allowed must remain false")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_decision_id": self.policy_decision_id,
            "policy_id": self.policy_id,
            "package_id": self.package_id,
            "signed_update_service_decision": self.signed_update_service_decision.to_dict(),
            "policy_accepted_for_next_gate": self.policy_accepted_for_next_gate,
            "update_signature_required": self.update_signature_required,
            "unsigned_update_allowed": self.unsigned_update_allowed,
            "snapshot_required_before_apply": self.snapshot_required_before_apply,
            "update_package_apply_allowed": self.update_package_apply_allowed,
            "security_layer_signature_replacement_allowed": self.security_layer_signature_replacement_allowed,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_default_update_recovery_policy() -> UpdateRecoveryPolicy:
    return UpdateRecoveryPolicy(
        policy_id=UPDATE_RECOVERY_POLICY_ID,
        update_signature_required=True,
        unsigned_update_allowed=False,
        snapshot_required_before_apply=True,
        direct_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        security_layer_signature_replacement_allowed=False,
        reason_codes=(
            "update_specific_signature_required",
            "unsigned_updates_forbidden",
            "snapshot_required_before_apply",
            "security_layer_signature_verifier_not_replaced",
        ),
    )


def evaluate_update_recovery_policy(
    *,
    policy: UpdateRecoveryPolicy,
    signed_update_service_decision: SignedUpdateServiceDecisionReadModel,
) -> UpdateRecoveryPolicyDecisionReadModel:
    if not isinstance(policy, UpdateRecoveryPolicy):
        raise TypeError("policy must be UpdateRecoveryPolicy")
    if not isinstance(signed_update_service_decision, SignedUpdateServiceDecisionReadModel):
        raise TypeError("signed_update_service_decision must be SignedUpdateServiceDecisionReadModel")

    accepted = signed_update_service_decision.signed_update_accepted

    reason_codes = (
        ("update_recovery_policy_accepts_signed_update_for_next_gate",)
        if accepted
        else ("update_recovery_policy_rejects_unsigned_or_untrusted_update",)
    ) + signed_update_service_decision.reason_codes

    return UpdateRecoveryPolicyDecisionReadModel(
        policy_decision_id=f"update_recovery_policy_decision:{signed_update_service_decision.package_id}",
        policy_id=policy.policy_id,
        package_id=signed_update_service_decision.package_id,
        signed_update_service_decision=signed_update_service_decision,
        policy_accepted_for_next_gate=accepted,
        update_signature_required=policy.update_signature_required,
        unsigned_update_allowed=policy.unsigned_update_allowed,
        snapshot_required_before_apply=policy.snapshot_required_before_apply,
        update_package_apply_allowed=False,
        security_layer_signature_replacement_allowed=policy.security_layer_signature_replacement_allowed,
        reason_codes=reason_codes,
    )


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        if not isinstance(reason_code, str):
            raise TypeError("reason_codes must contain strings")
        if not reason_code:
            raise ValueError("reason_codes must not contain empty values")
