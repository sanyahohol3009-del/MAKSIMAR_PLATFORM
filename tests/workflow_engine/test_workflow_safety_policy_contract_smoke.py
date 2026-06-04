import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    build_mobile_workflow_permission_profile,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import (
    build_approved_workflow_approval_ticket,
    build_pending_workflow_approval_ticket,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    WorkflowSafetyPolicyContract,
    build_workflow_safety_policy_contract,
)


def _proposal(risk_level: str = "medium") -> LocalAIWorkflowProposalContract:
    return build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.safety.001",
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create a governed workflow intent",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level=risk_level,
    )


def _permission_profile():
    return build_mobile_workflow_permission_profile(
        profile_id="profile.safety.android",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )


def test_workflow_safety_policy_allows_only_policy_gated_intent_creation() -> None:
    proposal = _proposal()
    profile = _permission_profile()
    approval = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.safety.001",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )
    policy = build_workflow_safety_policy_contract()

    decision = policy.evaluate_proposal(proposal, profile, approval)

    assert decision.allowed_for_intent_creation is True
    assert decision.decision_code == "allowed_for_intent_creation"
    assert policy.direct_phone_control_allowed is False
    assert policy.hidden_remote_control_allowed is False
    assert policy.direct_core_write_allowed is False
    assert policy.direct_server_canonical_write_allowed is False
    assert policy.network_socket_tunnel_allowed is False
    assert policy.dashboard_execution_allowed is False


def test_workflow_safety_policy_blocks_missing_permission_and_denied_permission() -> None:
    proposal = _proposal()
    policy = build_workflow_safety_policy_contract()
    approval = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.safety.002",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    assert policy.evaluate_proposal(proposal, None, approval).decision_code == "permission_required"

    denied_profile = build_mobile_workflow_permission_profile(
        profile_id="profile.denied",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal",),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )

    decision = policy.evaluate_proposal(proposal, denied_profile, approval)
    assert decision.allowed_for_intent_creation is False
    assert decision.decision_code == "permission_denied"
    assert decision.permission_decision is not None
    assert decision.permission_decision.reason_code == "capability_missing"


def test_workflow_safety_policy_blocks_missing_or_pending_approval() -> None:
    proposal = _proposal()
    profile = _permission_profile()
    policy = build_workflow_safety_policy_contract()

    assert policy.evaluate_proposal(proposal, profile, None).decision_code == "approval_required"

    pending = build_pending_workflow_approval_ticket(
        approval_ticket_id="approval.pending",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    assert policy.evaluate_proposal(proposal, profile, pending).decision_code == "approval_denied"


def test_workflow_safety_policy_blocks_critical_risk_and_unsafe_policy_flags() -> None:
    proposal = _proposal(risk_level="critical")
    profile = _permission_profile()
    approval = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.critical",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )
    policy = build_workflow_safety_policy_contract()

    assert policy.evaluate_proposal(proposal, profile, approval).decision_code == "critical_risk_blocked"

    unsafe_flags = (
        {"direct_phone_control_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"dashboard_execution_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowSafetyPolicyContract(**flag)
