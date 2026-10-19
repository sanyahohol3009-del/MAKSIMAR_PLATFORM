"""HOST-owned, exact-step approval continuation primitives.

This module is deliberately provider- and organ-neutral.  Pending approvals
are ephemeral execution-control state; they are not memory or semantic state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from threading import RLock
from typing import Any, Callable
from uuid import uuid4

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PermissionDecision


@dataclass(frozen=True, slots=True)
class PendingApproval:
    approval_id: str
    request_id: str
    session_id: str
    trace_id: str
    capability_id: str
    operation_id: str
    step_id: str
    risk_class: str
    effect_type: str
    description: str
    plan_step: dict[str, Any]
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    expires_at: str = ""

    def __post_init__(self) -> None:
        for name in ("approval_id", "request_id", "trace_id", "capability_id", "operation_id", "step_id", "risk_class", "effect_type", "description"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must not be empty")
        if self.status not in {"PENDING", "APPROVED", "DENIED", "CONSUMED", "EXPIRED"}:
            raise ValueError("invalid pending approval status")
        if not isinstance(self.plan_step, dict) or self.plan_step.get("step_id") != self.step_id:
            raise ValueError("pending approval must retain the exact PlanStep")

    def to_read_model(self) -> dict[str, Any]:
        # The executable PlanStep remains HOST-private.  Review surfaces get
        # only bounded identity/risk/action metadata, never parameters/locators.
        return {
            "approval_id": self.approval_id, "request_id": self.request_id,
            "session_id": self.session_id, "trace_id": self.trace_id,
            "capability_id": self.capability_id, "operation_id": self.operation_id,
            "step_id": self.step_id, "risk_class": self.risk_class,
            "effect_type": self.effect_type, "description": self.description,
            "status": self.status, "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


class HostApprovalStore:
    """Process-local HOST store with one-shot exact identity semantics."""

    def __init__(self, *, ttl_seconds: int = 900) -> None:
        self._ttl_seconds = ttl_seconds
        self._records: dict[str, PendingApproval] = {}
        self._callbacks: dict[str, Callable[[PermissionDecision], Any]] = {}
        self._lock = RLock()

    def create(
        self,
        *,
        request_id: str,
        session_id: str = "",
        decision: PermissionDecision,
        plan_step: dict[str, Any],
        description: str,
        resume: Callable[[PermissionDecision], Any] | None = None,
    ) -> PendingApproval:
        if not decision.approval_required or decision.granted:
            raise ValueError("pending approval requires an unresolved approval decision")
        if decision.step_id != str(plan_step.get("step_id", "")):
            raise ValueError("decision and PlanStep step_id must match")
        approval_id = f"approval_{uuid4().hex}"
        now = datetime.now(UTC)
        record = PendingApproval(
            approval_id=approval_id, request_id=request_id, session_id=session_id,
            trace_id=decision.trace_id, capability_id=decision.capability_id,
            operation_id=decision.operation_id, step_id=decision.step_id,
            risk_class=str(plan_step.get("risk_class", "UNKNOWN")),
            effect_type=str(plan_step.get("effect_type", "UNKNOWN")),
            description=description, plan_step=dict(plan_step),
            created_at=now.isoformat(),
            expires_at=(now + timedelta(seconds=self._ttl_seconds)).isoformat(),
        )
        with self._lock:
            self._records[approval_id] = record
            if resume is not None:
                self._callbacks[approval_id] = resume
        return record

    def get(self, approval_id: str) -> PendingApproval | None:
        with self._lock:
            record = self._records.get(approval_id)
            if record is None:
                return None
            if record.status == "PENDING" and record.expires_at:
                if datetime.fromisoformat(record.expires_at) <= datetime.now(UTC):
                    record = self._replace(record, status="EXPIRED")
                    self._records[approval_id] = record
            return record

    def decide(self, approval_id: str, *, approved: bool, approver_id: str,
               session_id: str = "") -> tuple[PendingApproval, PermissionDecision | None, Any]:
        if not approver_id.strip():
            raise ValueError("approver_id must not be empty")
        with self._lock:
            record = self.get(approval_id)
            if record is None:
                raise KeyError("unknown approval_id")
            if record.status != "PENDING":
                raise ValueError(f"approval is not pending: {record.status}")
            if record.session_id and record.session_id != session_id:
                raise ValueError("approval session does not match pending execution")
            status = "APPROVED" if approved else "DENIED"
            record = self._replace(record, status=status)
            self._records[approval_id] = record
            decision = PermissionDecision(
                granted=approved, capability_id=record.capability_id,
                identity_source=f"host_approval:{approver_id}", policy_version="semantic_policy.v1",
                denial_reason="" if approved else "approval_denied", trace_id=record.trace_id,
                operation_id=record.operation_id, approval_required=False,
                step_id=record.step_id,
            )
            if not approved:
                return record, decision, None
            callback = self._callbacks.pop(approval_id, None)
            if callback is None:
                return record, decision, None
            result = callback(decision)
            self._records[approval_id] = self._replace(record, status="CONSUMED")
            return self._records[approval_id], decision, result

    def pending_for_session(self, session_id: str) -> tuple[PendingApproval, ...]:
        """Read only this authenticated session's existing pending challenges."""
        if not session_id:
            return ()
        with self._lock:
            return tuple(
                record for approval_id in tuple(self._records)
                if (record := self.get(approval_id)) is not None
                and record.session_id == session_id and record.status == "PENDING"
            )

    @staticmethod
    def _replace(record: PendingApproval, **changes: Any) -> PendingApproval:
        values = {name: getattr(record, name) for name in record.__dataclass_fields__}
        values.update(changes)
        return PendingApproval(**values)


CANONICAL_HOST_APPROVAL_STORE = HostApprovalStore()

__all__ = ["PendingApproval", "HostApprovalStore", "CANONICAL_HOST_APPROVAL_STORE"]
