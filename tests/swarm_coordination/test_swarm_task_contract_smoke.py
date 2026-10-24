from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def test_swarm_task_contract_tracks_router_decision() -> None:
    route = route_swarm_task(SwarmTaskContract(
        "task", "typed test failure task", "text", "code_debug", "daily_coder_model", "jarvis:coder7b",
        ("repo_search", "pytest_report_read"), ("project_coder_agent",), "medium", False, False,
        False, True, "local_terminal_session", False))
    task = route.task_contract.to_read_model()

    assert task["normalized_intent"] == "code_debug"
    assert task["selected_model_role_id"] == "daily_coder_model"
    assert "repo_search" in task["selected_tools"]
    assert task["candidate_agent_roles"] == ("project_coder_agent",)
    assert task["read_only_discovery_only"] is True
    assert task["direct_execution_requested"] is False
