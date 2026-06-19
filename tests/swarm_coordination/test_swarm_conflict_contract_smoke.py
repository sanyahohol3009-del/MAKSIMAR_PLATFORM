from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
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
        claim_id="swarm_conflict_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_swarm_conflict_contract_blocks_heavy_parallel_agents() -> None:
    route_a = route_swarm_task(
        "сложный architecture traceback regression",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    route_b = route_swarm_task(
        "architecture traceback with complex regression",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    report = detect_swarm_conflicts((route_a, route_b))

    assert report.conflict_detected is True
    assert "heavy_gpu_parallel_blocked" in report.blocking_conflict_kinds
    assert report.heavy_gpu_lock_status == "parallel_heavy_agents_blocked"
