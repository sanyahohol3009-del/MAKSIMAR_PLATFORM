from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_approval_runtime import build_swarm_approval_decision
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def test_swarm_approval_runtime_returns_decision_not_execution() -> None:
    route = route_swarm_task(
        "open browser",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="swarm_safe_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    conflict_report = detect_swarm_conflicts((route,))
    approval = build_swarm_approval_decision(route, conflict_report).to_read_model()

    assert approval["approved"] is True
    assert approval["delegated_execution_surface"] == "action_library"
    assert approval["action_library_candidate"] is True
    assert approval["direct_execution_by_swarm"] is False
