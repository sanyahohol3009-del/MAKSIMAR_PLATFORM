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
class JuniorFeedbackIngestContract:
    contract_id: str
    junior_feedback_allowed: bool
    feedback_ingest_is_proposal_only: bool
    feedback_ingest_is_evidence_only: bool
    feedback_may_create_server_intent_candidate: bool
    feedback_may_execute_actions: bool
    feedback_may_write_canonical_memory: bool
    feedback_may_mutate_core: bool
    feedback_may_deploy: bool
    feedback_requires_server_review: bool
    owner_approval_required_for_mutation: bool
    no_cross_owner_leak: bool
    no_cross_tenant_leak: bool
    server_remains_canonical_authority: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        for field_name in (
            "junior_feedback_allowed",
            "feedback_ingest_is_proposal_only",
            "feedback_ingest_is_evidence_only",
            "feedback_may_create_server_intent_candidate",
            "feedback_requires_server_review",
            "owner_approval_required_for_mutation",
            "no_cross_owner_leak",
            "no_cross_tenant_leak",
            "server_remains_canonical_authority",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "feedback_may_execute_actions",
            "feedback_may_write_canonical_memory",
            "feedback_may_mutate_core",
            "feedback_may_deploy",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "junior_feedback_allowed": self.junior_feedback_allowed,
            "feedback_ingest_is_proposal_only": self.feedback_ingest_is_proposal_only,
            "feedback_ingest_is_evidence_only": self.feedback_ingest_is_evidence_only,
            "feedback_may_create_server_intent_candidate": self.feedback_may_create_server_intent_candidate,
            "feedback_may_execute_actions": self.feedback_may_execute_actions,
            "feedback_may_write_canonical_memory": self.feedback_may_write_canonical_memory,
            "feedback_may_mutate_core": self.feedback_may_mutate_core,
            "feedback_may_deploy": self.feedback_may_deploy,
            "feedback_requires_server_review": self.feedback_requires_server_review,
            "owner_approval_required_for_mutation": self.owner_approval_required_for_mutation,
            "no_cross_owner_leak": self.no_cross_owner_leak,
            "no_cross_tenant_leak": self.no_cross_tenant_leak,
            "server_remains_canonical_authority": self.server_remains_canonical_authority,
        }


def build_junior_feedback_ingest_contract() -> JuniorFeedbackIngestContract:
    return JuniorFeedbackIngestContract(
        contract_id="junior_feedback_ingest_contract_v0_1",
        junior_feedback_allowed=True,
        feedback_ingest_is_proposal_only=True,
        feedback_ingest_is_evidence_only=True,
        feedback_may_create_server_intent_candidate=True,
        feedback_may_execute_actions=False,
        feedback_may_write_canonical_memory=False,
        feedback_may_mutate_core=False,
        feedback_may_deploy=False,
        feedback_requires_server_review=True,
        owner_approval_required_for_mutation=True,
        no_cross_owner_leak=True,
        no_cross_tenant_leak=True,
        server_remains_canonical_authority=True,
    )
