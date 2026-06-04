from ANDROID_SHELL.workflow_adapter.android_local_workflow_intent_client import (
    build_android_local_workflow_intent_client,
)
from ANDROID_SHELL.workflow_adapter.android_workflow_permission_bridge import (
    build_android_workflow_permission_bridge,
)
from IOS_SHELL.workflow_adapter.ios_local_workflow_intent_client import (
    build_ios_local_workflow_intent_client,
)
from IOS_SHELL.workflow_adapter.ios_workflow_permission_bridge import (
    build_ios_workflow_permission_bridge,
)
from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import (
    build_approved_workflow_approval_ticket,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import WorkflowAuditEventContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def _proposal(proposal_id: str):
    return build_local_ai_workflow_proposal_contract(
        proposal_id=proposal_id,
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create mobile local workflow intent metadata",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )


def _approval(proposal):
    return build_approved_workflow_approval_ticket(
        approval_ticket_id=f"approval.{proposal.proposal_id}",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )


def _audit(proposal):
    return WorkflowAuditEventContract(
        audit_event_id=f"audit.{proposal.proposal_id}",
        proposal_id=proposal.proposal_id,
        actor_id="owner",
        event_type="approval_granted",
        event_result="allowed",
        decision_reason="mobile local workflow approval granted",
        sequence=1,
    )


def test_android_local_workflow_requires_explicit_permission_before_intent() -> None:
    proposal = _proposal("proposal.android.explicit.permission")
    bridge = build_android_workflow_permission_bridge(
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    client = build_android_local_workflow_intent_client(permission_bridge=bridge)

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=_approval(proposal),
        audit_event=_audit(proposal),
    )

    assert decision.allowed_for_local_intent is False
    assert decision.decision_code == "permission_denied"
    assert decision.safety_decision.permission_decision is not None
    assert decision.safety_decision.permission_decision.reason_code == "explicit_permission_missing"
    assert decision.execution_performed is False


def test_ios_local_workflow_requires_explicit_permission_before_intent() -> None:
    proposal = _proposal("proposal.ios.explicit.permission")
    bridge = build_ios_workflow_permission_bridge(
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    client = build_ios_local_workflow_intent_client(permission_bridge=bridge)

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=_approval(proposal),
        audit_event=_audit(proposal),
    )

    assert decision.allowed_for_local_intent is False
    assert decision.decision_code == "permission_denied"
    assert decision.safety_decision.permission_decision is not None
    assert decision.safety_decision.permission_decision.reason_code == "explicit_permission_missing"
    assert decision.execution_performed is False
