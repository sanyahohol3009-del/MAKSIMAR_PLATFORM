import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def test_local_ai_workflow_proposal_is_deterministic_and_not_execution_authority() -> None:
    graph = build_sample_workflow_graph_contract()
    proposal = build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.local.001",
        requester_id="owner",
        graph=graph,
        natural_language_goal="Prepare a local workflow proposal",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )

    assert proposal.proposal_state == "awaiting_permission"
    assert proposal.requires_permission is True
    assert proposal.requires_user_approval is True
    assert proposal.sandbox_preview_required is True
    assert proposal.audit_required is True
    assert proposal.proposal_is_execution_authority is False
    assert proposal.execution_authority_allowed is False
    assert proposal.direct_core_write_allowed is False
    assert proposal.direct_server_canonical_write_allowed is False
    assert proposal.network_socket_tunnel_allowed is False
    assert proposal.hidden_remote_control_allowed is False
    assert proposal.proposal_fingerprint() == proposal.proposal_fingerprint()
    assert len(proposal.proposal_fingerprint()) == 64


def test_local_ai_workflow_proposal_rejects_empty_and_invalid_fields() -> None:
    graph = build_sample_workflow_graph_contract()

    with pytest.raises(ValueError):
        LocalAIWorkflowProposalContract(
            proposal_id="",
            requester_id="owner",
            graph=graph,
            natural_language_goal="Goal",
            requested_capability_refs=("local_ai_workflow_proposal",),
            risk_level="medium",
        )

    with pytest.raises(ValueError):
        LocalAIWorkflowProposalContract(
            proposal_id="proposal.invalid.risk",
            requester_id="owner",
            graph=graph,
            natural_language_goal="Goal",
            requested_capability_refs=("local_ai_workflow_proposal",),
            risk_level="unbounded",
        )

    with pytest.raises(ValueError):
        LocalAIWorkflowProposalContract(
            proposal_id="proposal.empty.capabilities",
            requester_id="owner",
            graph=graph,
            natural_language_goal="Goal",
            requested_capability_refs=(),
            risk_level="medium",
        )


def test_local_ai_workflow_proposal_rejects_runtime_authority_flags() -> None:
    graph = build_sample_workflow_graph_contract()
    unsafe_flags = (
        {"proposal_is_execution_authority": True},
        {"execution_authority_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            LocalAIWorkflowProposalContract(
                proposal_id=f"proposal.{next(iter(flag))}",
                requester_id="owner",
                graph=graph,
                natural_language_goal="Unsafe proposal",
                requested_capability_refs=("local_ai_workflow_proposal",),
                risk_level="medium",
                **flag,
            )
