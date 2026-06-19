from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_terminal,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    claim = build_owner_identity_claim_for_terminal()
    if claim.verified:
        return claim
    return OwnerIdentityClaim(
        claim_id="swarm_task_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_swarm_task_contract_tracks_router_decision() -> None:
    route = route_swarm_task(
        "Джарвис, pytest упал, проверь ошибку",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    task = route.task_contract.to_read_model()

    assert task["normalized_intent"] == "code_debug"
    assert task["selected_model_role_id"] == "daily_coder_model"
    assert "repo_search" in task["selected_tools"]
    assert task["candidate_agent_roles"] == ("project_coder_agent",)
    assert task["read_only_discovery_only"] is True
    assert task["direct_execution_requested"] is False
