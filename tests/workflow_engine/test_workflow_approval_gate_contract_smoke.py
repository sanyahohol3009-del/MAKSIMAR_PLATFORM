import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import (
    WorkflowApprovalGateContract,
    build_approved_workflow_approval_ticket,
    build_pending_workflow_approval_ticket,
)


def test_workflow_approval_gate_blocks_until_explicit_approval_and_preview_review() -> None:
    pending = build_pending_workflow_approval_ticket(
        approval_ticket_id="approval.pending.001",
        proposal_id="proposal.001",
        approver_id="owner",
        risk_level="medium",
    )

    assert pending.allows_intent_creation("proposal.001") is False

    approved = build_approved_workflow_approval_ticket(
        approval_ticket_id="approval.approved.001",
        proposal_id="proposal.001",
        approver_id="owner",
        risk_level="medium",
    )

    assert approved.allows_intent_creation("proposal.001") is True
    assert approved.execution_authority_allowed is False
    assert approved.direct_phone_control_allowed is False
    assert approved.hidden_remote_control_allowed is False
    assert approved.direct_core_write_allowed is False
    assert approved.direct_server_canonical_write_allowed is False
    assert approved.network_socket_tunnel_allowed is False


def test_workflow_approval_gate_rejects_approved_ticket_without_required_evidence() -> None:
    with pytest.raises(ValueError):
        WorkflowApprovalGateContract(
            approval_ticket_id="approval.no.user",
            proposal_id="proposal.001",
            approver_id="owner",
            decision="approved",
            approval_scope="single_run_intent",
            risk_level="medium",
            explicit_user_approval_present=False,
            sandbox_preview_reviewed=True,
        )

    with pytest.raises(ValueError):
        WorkflowApprovalGateContract(
            approval_ticket_id="approval.no.preview",
            proposal_id="proposal.001",
            approver_id="owner",
            decision="approved",
            approval_scope="single_run_intent",
            risk_level="medium",
            explicit_user_approval_present=True,
            sandbox_preview_reviewed=False,
        )


def test_workflow_approval_gate_rejects_unsafe_authority_flags() -> None:
    unsafe_flags = (
        {"execution_authority_allowed": True},
        {"direct_phone_control_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowApprovalGateContract(
                approval_ticket_id=f"approval.{next(iter(flag))}",
                proposal_id="proposal.001",
                approver_id="owner",
                decision="pending",
                approval_scope="preview_only",
                risk_level="medium",
                explicit_user_approval_present=False,
                sandbox_preview_reviewed=False,
                **flag,
            )
