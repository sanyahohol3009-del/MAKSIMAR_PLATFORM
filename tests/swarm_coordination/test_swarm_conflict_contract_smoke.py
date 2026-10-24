from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def _heavy(task_id: str) -> SwarmTaskContract:
    return SwarmTaskContract(task_id, "typed architecture task", "text", "complex_code_analysis",
        "heavy_coder_model", "jarvis:coder14b", ("repo_search",), ("architect_agent",),
        "heavy", True, False, False, True, "local_terminal_session", False)


def test_swarm_conflict_contract_blocks_heavy_parallel_agents() -> None:
    route_a = route_swarm_task(_heavy("task-a"))
    route_b = route_swarm_task(_heavy("task-b"))
    report = detect_swarm_conflicts((route_a, route_b))

    assert report.conflict_detected is True
    assert "heavy_gpu_parallel_blocked" in report.blocking_conflict_kinds
    assert report.heavy_gpu_lock_status == "parallel_heavy_agents_blocked"
