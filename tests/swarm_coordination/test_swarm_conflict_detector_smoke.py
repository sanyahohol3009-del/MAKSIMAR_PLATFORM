from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="swarm_conflict_verified_terminal_v2",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_swarm_conflict_detector_blocks_voice_unverified_pc_action_and_unknown_tools() -> None:
    voice_browser = route_swarm_task(
        "open browser",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
    )
    unknown = route_swarm_task(
        "pytest failure",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    object.__setattr__(unknown, "selected_tools", ("unknown_side_effect_tool",))
    report = detect_swarm_conflicts((voice_browser, unknown))

    assert report.conflict_detected is True
    assert "voice_unverified_direct_pc_action_blocked" in report.blocking_conflict_kinds
    assert "unknown_tool_with_side_effects_blocked" in report.blocking_conflict_kinds
    assert report.risk_gate_required is True
