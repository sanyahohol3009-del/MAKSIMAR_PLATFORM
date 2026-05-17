from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityRequest,
    SecurityRiskLevel,
)


class SecurityDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    NEEDS_APPROVAL = "needs_approval"
    NEEDS_SIGNATURE = "needs_signature"
    NEEDS_VOICE_IDENTITY = "needs_voice_identity"


@dataclass(frozen=True, slots=True)
class SecurityDecision:
    request_id: str
    trace_id: str
    status: SecurityDecisionStatus
    risk_level: SecurityRiskLevel
    reason_codes: tuple[str, ...]
    human_summary: str
    approval_required: bool
    voice_identity_required: bool
    signature_required: bool
    action_execution_allowed: bool
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("human_summary", self.human_summary),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.status, SecurityDecisionStatus):
            raise TypeError("status must be SecurityDecisionStatus")
        if not isinstance(self.risk_level, SecurityRiskLevel):
            raise TypeError("risk_level must be SecurityRiskLevel")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.status is not SecurityDecisionStatus.ALLOW and self.action_execution_allowed:
            raise ValueError("only ALLOW decisions may permit action execution")
        if self.status is SecurityDecisionStatus.ALLOW:
            if self.approval_required or self.voice_identity_required or self.signature_required:
                raise ValueError("ALLOW decision must not have unresolved requirements")


@dataclass(frozen=True, slots=True)
class SecurityDecisionReadModel:
    request_id: str
    trace_id: str
    status: str
    risk_level: str
    reason_codes: tuple[str, ...]
    human_summary: str
    approval_required: bool
    voice_identity_required: bool
    signature_required: bool
    action_execution_allowed: bool
    dashboard_safe: bool
    runtime_mutation_allowed: bool
    canonical_write_allowed: bool

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.trace_id:
            raise ValueError("trace_id must not be empty")
        if not self.status:
            raise ValueError("status must not be empty")
        if not self.risk_level:
            raise ValueError("risk_level must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reason_codes"] = list(self.reason_codes)
        return payload


def build_security_decision_read_model(
    decision: SecurityDecision,
) -> SecurityDecisionReadModel:
    return SecurityDecisionReadModel(
        request_id=decision.request_id,
        trace_id=decision.trace_id,
        status=decision.status.value,
        risk_level=decision.risk_level.value,
        reason_codes=decision.reason_codes,
        human_summary=decision.human_summary,
        approval_required=decision.approval_required,
        voice_identity_required=decision.voice_identity_required,
        signature_required=decision.signature_required,
        action_execution_allowed=decision.action_execution_allowed,
        dashboard_safe=decision.dashboard_safe,
        runtime_mutation_allowed=decision.runtime_mutation_allowed,
        canonical_write_allowed=decision.canonical_write_allowed,
    )


def deny_security_request(
    request: SecurityRequest,
    *,
    reason_codes: tuple[str, ...],
    human_summary: str,
) -> SecurityDecision:
    return SecurityDecision(
        request_id=request.context.request_id,
        trace_id=request.context.trace_id,
        status=SecurityDecisionStatus.DENY,
        risk_level=request.risk_level,
        reason_codes=reason_codes,
        human_summary=human_summary,
        approval_required=request.requires_approval,
        voice_identity_required=request.requires_voice_identity,
        signature_required=request.requires_signature,
        action_execution_allowed=False,
    )
