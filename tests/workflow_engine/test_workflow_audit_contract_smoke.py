import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import (
    WorkflowAuditEventContract,
    WorkflowAuditTrailContract,
)


def test_workflow_audit_event_is_deterministic_read_only_and_immutable() -> None:
    event = WorkflowAuditEventContract(
        audit_event_id="audit.event.001",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="proposal_created",
        event_result="recorded",
        decision_reason="proposal created for review",
        sequence=1,
        evidence_refs=("proposal.001",),
    )

    assert event.event_fingerprint() == event.event_fingerprint()
    assert len(event.event_fingerprint()) == 64
    assert event.immutable_event is True
    assert event.read_only is True
    assert event.contract_only is True
    assert event.runtime_mutation_allowed is False
    assert event.direct_core_write_allowed is False
    assert event.direct_server_canonical_write_allowed is False


def test_workflow_audit_trail_is_append_only_and_sequence_checked() -> None:
    first = WorkflowAuditEventContract(
        audit_event_id="audit.event.001",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="proposal_created",
        event_result="recorded",
        decision_reason="proposal created for review",
        sequence=1,
    )
    second = WorkflowAuditEventContract(
        audit_event_id="audit.event.002",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="permission_evaluated",
        event_result="allowed",
        decision_reason="permission profile allowed proposal",
        sequence=2,
    )

    trail = WorkflowAuditTrailContract(
        trail_id="audit.trail.001",
        proposal_id="proposal.001",
        events=(first,),
    )
    updated = trail.append_event(second)

    assert len(trail.events) == 1
    assert len(updated.events) == 2
    assert updated.to_read_model()["event_count"] == 2


def test_workflow_audit_trail_rejects_duplicate_or_regressing_events() -> None:
    first = WorkflowAuditEventContract(
        audit_event_id="audit.event.001",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="proposal_created",
        event_result="recorded",
        decision_reason="proposal created for review",
        sequence=1,
    )
    duplicate_id = WorkflowAuditEventContract(
        audit_event_id="audit.event.001",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="permission_evaluated",
        event_result="allowed",
        decision_reason="permission allowed",
        sequence=2,
    )
    regressing = WorkflowAuditEventContract(
        audit_event_id="audit.event.003",
        proposal_id="proposal.001",
        actor_id="owner",
        event_type="approval_requested",
        event_result="recorded",
        decision_reason="approval requested",
        sequence=1,
    )

    with pytest.raises(ValueError):
        WorkflowAuditTrailContract(
            trail_id="audit.trail.duplicate",
            proposal_id="proposal.001",
            events=(first, duplicate_id),
        )

    trail = WorkflowAuditTrailContract(
        trail_id="audit.trail.regression",
        proposal_id="proposal.001",
        events=(first,),
    )
    with pytest.raises(ValueError):
        trail.append_event(regressing)


def test_workflow_audit_event_rejects_mutation_flags() -> None:
    with pytest.raises(ValueError):
        WorkflowAuditEventContract(
            audit_event_id="audit.event.mutable",
            proposal_id="proposal.001",
            actor_id="owner",
            event_type="proposal_created",
            event_result="recorded",
            decision_reason="invalid mutable event",
            sequence=1,
            runtime_mutation_allowed=True,
        )
