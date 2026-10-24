from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def test_swarm_conflict_detector_blocks_voice_unverified_pc_action_and_unknown_tools() -> None:
    voice_browser = route_swarm_task(SwarmTaskContract(
        "voice", "typed pc step", "voice", "safe_pc_open_browser", "jarvis_chat_model", "jarvis:chat8b",
        ("pc_open_browser",), ("action_worker_agent",), "light", False, True, False, False,
        "voice_unverified", True))
    unknown = route_swarm_task(SwarmTaskContract(
        "unknown", "typed unknown step", "text", "code_debug", "daily_coder_model", "jarvis:coder7b",
        ("repo_search",), ("project_coder_agent",), "medium", False, False, False, True,
        "local_terminal_session", False))
    object.__setattr__(unknown, "selected_tools", ("unknown_side_effect_tool",))
    report = detect_swarm_conflicts((voice_browser, unknown))

    assert report.conflict_detected is True
    assert "voice_unverified_direct_pc_action_blocked" in report.blocking_conflict_kinds
    assert "unknown_tool_with_side_effects_blocked" in report.blocking_conflict_kinds
    assert report.risk_gate_required is True
