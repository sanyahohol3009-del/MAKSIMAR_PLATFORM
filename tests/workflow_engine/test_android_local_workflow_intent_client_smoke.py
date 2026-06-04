from ANDROID_SHELL.workflow_adapter.android_local_workflow_intent_client import (
    build_android_local_workflow_intent_client,
)
from ANDROID_SHELL.workflow_adapter.android_workflow_permission_bridge import (
    build_android_workflow_permission_bridge,
)
from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import (
    build_approved_workflow_approval_ticket,
    build_pending_workflow_approval_ticket,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import WorkflowAuditEventContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def _proposal():
    return build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.android.intent.001",
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create Android local workflow intent metadata",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )


def _audit_event(proposal_id: str):
    return WorkflowAuditEventContract(
        audit_event_id="audit.android.intent.001",
        proposal_id=proposal_id,
        actor_id="owner",
        event_type="approval_granted",
        event_result="allowed",
        decision_reason="Android local workflow approval granted",
        sequence=1,
    )


def test_android_local_workflow_intent_client_creates_metadata_only_local_intent() -> None:
    bridge = build_android_workflow_permission_bridge(
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    client = build_android_local_workflow_intent_client(permission_bridge=bridge)
    proposal = _proposal()
    approval = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.android.intent.001",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=approval,
        audit_event=_audit_event(proposal.proposal_id),
    )

    assert decision.allowed_for_local_intent is True
    assert decision.decision_code == "allowed_for_intent_creation"
    assert decision.metadata_only is True
    assert decision.local_first is True
    assert decision.server_optional is True
    assert decision.execution_performed is False
    assert decision.direct_phone_control_allowed is False
    assert decision.hidden_remote_control_allowed is False
    assert len(decision.intent_fingerprint()) == 64


def test_android_local_workflow_intent_client_blocks_pending_approval() -> None:
    bridge = build_android_workflow_permission_bridge(
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    client = build_android_local_workflow_intent_client(permission_bridge=bridge)
    proposal = _proposal()
    pending = build_pending_workflow_approval_ticket(
        approval_ticket_id="approval.android.pending",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=pending,
        audit_event=_audit_event(proposal.proposal_id),
    )

    assert decision.allowed_for_local_intent is False
    assert decision.decision_code == "approval_denied"
    assert decision.execution_performed is False
