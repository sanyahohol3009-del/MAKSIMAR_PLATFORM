from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_approval_runtime import build_swarm_approval_decision
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="phase10_verified_terminal_claim_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_phase_10_acceptance_smoke() -> None:
    doc_path = Path("docs/architecture/swarm_coordination/phase_10_swarm_acceptance_v1.md")
    assert doc_path.exists()

    weather = route_swarm_task(
        "weather in Berlin",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    heavy_a = route_swarm_task(
        "architecture traceback regression",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    heavy_b = route_swarm_task(
        "complex architecture traceback",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    voice_browser = route_swarm_task(
        "open browser",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
    )
    terminal_browser = route_swarm_task(
        "open browser",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    heavy_conflict = detect_swarm_conflicts((heavy_a, heavy_b))
    voice_conflict = detect_swarm_conflicts((voice_browser,))
    terminal_conflict = detect_swarm_conflicts((terminal_browser,))
    terminal_approval = build_swarm_approval_decision(terminal_browser, terminal_conflict).to_read_model()

    assert weather.selected_agent_role == "tool_selector_agent"
    assert weather.selected_model_id == "jarvis:chat8b"
    assert weather.selected_tools == ("weather_lookup",)
    assert terminal_browser.direct_execution_disabled is True
    assert "heavy_gpu_parallel_blocked" in heavy_conflict.blocking_conflict_kinds
    assert "voice_unverified_direct_pc_action_blocked" in voice_conflict.blocking_conflict_kinds
    assert terminal_approval["approved"] is True
    assert terminal_approval["delegated_execution_surface"] == "action_library"
    assert terminal_approval["direct_execution_by_swarm"] is False
