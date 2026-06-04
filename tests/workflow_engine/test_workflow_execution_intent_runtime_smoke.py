import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    build_mobile_workflow_permission_profile,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import (
    build_approved_workflow_approval_ticket,
    build_pending_workflow_approval_ticket,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import WorkflowAuditEventContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    build_workflow_safety_policy_contract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import build_n8n_adapter_contract
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.workflow_execution_intent_runtime import (
    WorkflowExecutionIntentRecord,
    WorkflowExecutionIntentRuntime,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.workflow_runtime_policy import (
    build_workflow_runtime_policy,
)


def _proposal():
    return build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.runtime.001",
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create governed intent metadata",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )


def _permission_profile():
    return build_mobile_workflow_permission_profile(
        profile_id="profile.runtime.android",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )


def _audit_event(proposal_id: str):
    return WorkflowAuditEventContract(
        audit_event_id="audit.runtime.001",
        proposal_id=proposal_id,
        actor_id="owner",
        event_type="approval_granted",
        event_result="allowed",
        decision_reason="approval granted for policy-gated intent metadata",
        sequence=1,
    )


def test_workflow_execution_intent_runtime_creates_metadata_only_intent() -> None:
    adapter = build_n8n_adapter_contract()
    runtime = WorkflowExecutionIntentRuntime(
        runtime_id="runtime.intent.001",
        adapter=adapter,
        runtime_policy=build_workflow_runtime_policy(adapter),
        safety_policy=build_workflow_safety_policy_contract(),
    )
    proposal = _proposal()
    approval = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.runtime.001",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    intent = runtime.create_policy_gated_intent(
        intent_id="intent.runtime.001",
        proposal=proposal,
        permission_profile=_permission_profile(),
        approval_ticket=approval,
        audit_event=_audit_event(proposal.proposal_id),
    )

    assert intent.intent_state == "created"
    assert intent.metadata_only is True
    assert intent.single_run_intent is True
    assert intent.policy_gated is True
    assert intent.runtime_execution_allowed_now is False
    assert intent.direct_core_write_allowed is False
    assert intent.direct_server_canonical_write_allowed is False
    assert intent.network_allowed is False
    assert len(intent.intent_fingerprint()) == 64


def test_workflow_execution_intent_runtime_blocks_pending_approval() -> None:
    adapter = build_n8n_adapter_contract()
    runtime = WorkflowExecutionIntentRuntime(
        runtime_id="runtime.intent.blocked",
        adapter=adapter,
        runtime_policy=build_workflow_runtime_policy(adapter),
        safety_policy=build_workflow_safety_policy_contract(),
    )
    proposal = _proposal()
    pending = build_pending_workflow_approval_ticket(
        approval_ticket_id="approval.pending.runtime",
        proposal_id=proposal.proposal_id,
        approver_id="owner",
        risk_level=proposal.risk_level,
    )

    intent = runtime.create_policy_gated_intent(
        intent_id="intent.runtime.blocked",
        proposal=proposal,
        permission_profile=_permission_profile(),
        approval_ticket=pending,
        audit_event=_audit_event(proposal.proposal_id),
    )

    assert intent.intent_state == "blocked"
    assert intent.safety_decision_code == "approval_denied"
    assert intent.runtime_execution_allowed_now is False


def test_workflow_execution_intent_record_rejects_runtime_authority_flags() -> None:
    unsafe_flags = (
        {"runtime_execution_allowed_now": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"dashboard_execution_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_phone_control_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowExecutionIntentRecord(
                intent_id=f"intent.{next(iter(flag))}",
                proposal_id="proposal.001",
                graph_id="graph.001",
                adapter_id="adapter.001",
                execution_tier="mobile_local",
                intent_state="created",
                safety_decision_code="allowed_for_intent_creation",
                audit_event_id="audit.001",
                **flag,
            )
