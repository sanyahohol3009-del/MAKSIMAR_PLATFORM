from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_approval_runtime import build_swarm_approval_decision
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def test_swarm_approval_runtime_returns_decision_not_execution() -> None:
    route = route_swarm_task(SwarmTaskContract(
        "task", "typed pc step", "text", "safe_pc_open_browser", "jarvis_chat_model", "jarvis:chat8b",
        ("pc_open_browser",), ("action_worker_agent",), "light", False, False, True, False,
        "local_terminal_session", True,
    ))
    conflict_report = detect_swarm_conflicts((route,))
    approval = build_swarm_approval_decision(route, conflict_report).to_read_model()

    assert approval["approved"] is True
    assert approval["delegated_execution_surface"] == "action_library"
    assert approval["action_library_candidate"] is True
    assert approval["direct_execution_by_swarm"] is False
