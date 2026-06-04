from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Tuple


ALLOWED_WORKFLOW_AUDIT_EVENT_TYPES: Tuple[str, ...] = (
    "proposal_created",
    "permission_evaluated",
    "approval_requested",
    "approval_granted",
    "approval_rejected",
    "safety_allowed",
    "safety_rejected",
    "intent_created",
)
ALLOWED_WORKFLOW_AUDIT_RESULTS: Tuple[str, ...] = ("recorded", "allowed", "blocked")


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class WorkflowAuditEventContract:
    audit_event_id: str
    proposal_id: str
    actor_id: str
    event_type: str
    event_result: str
    decision_reason: str
    sequence: int
    evidence_refs: Tuple[str, ...] = ()
    immutable_event: bool = True
    read_only: bool = True
    contract_only: bool = True
    runtime_mutation_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "audit_event_id", _require_non_empty_text(self.audit_event_id, "audit_event_id"))
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "actor_id", _require_non_empty_text(self.actor_id, "actor_id"))
        object.__setattr__(
            self,
            "event_type",
            _require_allowed(self.event_type, "event_type", ALLOWED_WORKFLOW_AUDIT_EVENT_TYPES),
        )
        object.__setattr__(
            self,
            "event_result",
            _require_allowed(self.event_result, "event_result", ALLOWED_WORKFLOW_AUDIT_RESULTS),
        )
        object.__setattr__(self, "decision_reason", _require_non_empty_text(self.decision_reason, "decision_reason"))
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise ValueError("sequence must be a positive integer")
        object.__setattr__(self, "evidence_refs", _normalize_text_tuple(self.evidence_refs, "evidence_refs"))

        if self.immutable_event is not True:
            raise ValueError("immutable_event must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.contract_only is not True:
            raise ValueError("contract_only must be True")
        if self.runtime_mutation_allowed is not False:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed is not False:
            raise ValueError("direct_core_write_allowed must be False")
        if self.direct_server_canonical_write_allowed is not False:
            raise ValueError("direct_server_canonical_write_allowed must be False")

    def event_fingerprint(self) -> str:
        payload = {
            "audit_event_id": self.audit_event_id,
            "proposal_id": self.proposal_id,
            "actor_id": self.actor_id,
            "event_type": self.event_type,
            "event_result": self.event_result,
            "decision_reason": self.decision_reason,
            "sequence": self.sequence,
            "evidence_refs": self.evidence_refs,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_read_model(self) -> dict[str, object]:
        return {
            "audit_event_id": self.audit_event_id,
            "proposal_id": self.proposal_id,
            "actor_id": self.actor_id,
            "event_type": self.event_type,
            "event_result": self.event_result,
            "decision_reason": self.decision_reason,
            "sequence": self.sequence,
            "evidence_refs": self.evidence_refs,
            "event_fingerprint": self.event_fingerprint(),
            "immutable_event": self.immutable_event,
            "read_only": self.read_only,
            "contract_only": self.contract_only,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
        }


@dataclass(frozen=True)
class WorkflowAuditTrailContract:
    trail_id: str
    proposal_id: str
    events: Tuple[WorkflowAuditEventContract, ...]
    append_only: bool = True
    read_only_projection: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "trail_id", _require_non_empty_text(self.trail_id, "trail_id"))
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        if not isinstance(self.events, tuple):
            raise TypeError("events must be a tuple of WorkflowAuditEventContract objects")
        if self.append_only is not True:
            raise ValueError("append_only must be True")
        if self.read_only_projection is not True:
            raise ValueError("read_only_projection must be True")

        event_ids = tuple(event.audit_event_id for event in self.events)
        if len(set(event_ids)) != len(event_ids):
            raise ValueError("audit trail event ids must be unique")

        sequences = tuple(event.sequence for event in self.events)
        if sequences != tuple(sorted(sequences)):
            raise ValueError("audit trail event sequences must be monotonic")

        for event in self.events:
            if not isinstance(event, WorkflowAuditEventContract):
                raise TypeError("events must contain only WorkflowAuditEventContract objects")
            if event.proposal_id != self.proposal_id:
                raise ValueError("all audit events must match the trail proposal_id")

    def append_event(self, event: WorkflowAuditEventContract) -> "WorkflowAuditTrailContract":
        if not isinstance(event, WorkflowAuditEventContract):
            raise TypeError("event must be a WorkflowAuditEventContract")
        if event.proposal_id != self.proposal_id:
            raise ValueError("event proposal_id must match audit trail proposal_id")
        if self.events and event.sequence <= self.events[-1].sequence:
            raise ValueError("appended audit event sequence must be greater than the current last sequence")
        return WorkflowAuditTrailContract(
            trail_id=self.trail_id,
            proposal_id=self.proposal_id,
            events=self.events + (event,),
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "trail_id": self.trail_id,
            "proposal_id": self.proposal_id,
            "event_count": len(self.events),
            "events": tuple(event.to_read_model() for event in self.events),
            "append_only": self.append_only,
            "read_only_projection": self.read_only_projection,
        }


__all__ = [
    "ALLOWED_WORKFLOW_AUDIT_EVENT_TYPES",
    "ALLOWED_WORKFLOW_AUDIT_RESULTS",
    "WorkflowAuditEventContract",
    "WorkflowAuditTrailContract",
]
