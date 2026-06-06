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


def test_phase_6_android_mobile_local_workflow_acceptance_path_is_policy_gated() -> None:
    proposal = _proposal("proposal.phase6.android.acceptance")
    bridge = build_android_workflow_permission_bridge(
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    client = build_android_local_workflow_intent_client(permission_bridge=bridge)

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=_approval(proposal),
        audit_event=_audit(proposal),
    )

    assert decision.allowed_for_local_intent is True
    assert decision.metadata_only is True
    assert decision.local_first is True
    assert decision.server_optional is True
    assert decision.offline_queue_eligible is True
    assert decision.execution_performed is False
    assert decision.direct_phone_control_allowed is False
    assert decision.hidden_remote_control_allowed is False
    assert decision.direct_core_write_allowed is False
    assert decision.direct_server_canonical_write_allowed is False
    assert decision.network_allowed_by_default is False
    assert decision.socket_allowed_by_default is False
    assert decision.tunnel_allowed_by_default is False
    assert decision.runtime_mutation_allowed is False


def test_phase_6_ios_mobile_local_workflow_acceptance_path_is_policy_gated() -> None:
    proposal = _proposal("proposal.phase6.ios.acceptance")
    bridge = build_ios_workflow_permission_bridge(
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    client = build_ios_local_workflow_intent_client(permission_bridge=bridge)

    decision = client.request_local_workflow_intent(
        proposal=proposal,
        approval_ticket=_approval(proposal),
        audit_event=_audit(proposal),
    )

    assert decision.allowed_for_local_intent is True
    assert decision.metadata_only is True
    assert decision.local_first is True
    assert decision.server_optional is True
    assert decision.offline_queue_eligible is True
    assert decision.execution_performed is False
    assert decision.direct_phone_control_allowed is False
    assert decision.hidden_remote_control_allowed is False
    assert decision.direct_core_write_allowed is False
    assert decision.direct_server_canonical_write_allowed is False
    assert decision.network_allowed_by_default is False
    assert decision.socket_allowed_by_default is False
    assert decision.tunnel_allowed_by_default is False
    assert decision.runtime_mutation_allowed is False


def test_phase_6_mobile_local_workflow_rejects_missing_explicit_permission() -> None:
    android_proposal = _proposal("proposal.phase6.android.no.permission")
    android_bridge = build_android_workflow_permission_bridge(
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    android_client = build_android_local_workflow_intent_client(permission_bridge=android_bridge)
    android_decision = android_client.request_local_workflow_intent(
        proposal=android_proposal,
        approval_ticket=_approval(android_proposal),
        audit_event=_audit(android_proposal),
    )

    ios_proposal = _proposal("proposal.phase6.ios.no.permission")
    ios_bridge = build_ios_workflow_permission_bridge(
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    ios_client = build_ios_local_workflow_intent_client(permission_bridge=ios_bridge)
    ios_decision = ios_client.request_local_workflow_intent(
        proposal=ios_proposal,
        approval_ticket=_approval(ios_proposal),
        audit_event=_audit(ios_proposal),
    )

    assert android_decision.allowed_for_local_intent is False
    assert android_decision.decision_code == "permission_denied"
    assert ios_decision.allowed_for_local_intent is False
    assert ios_decision.decision_code == "permission_denied"
