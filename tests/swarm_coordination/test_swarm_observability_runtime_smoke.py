from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_observability_runtime import (
    build_swarm_observability_read_model,
)
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def test_swarm_observability_runtime_exposes_required_read_model_fields() -> None:
    route = route_swarm_task(SwarmTaskContract(
        "task", "typed pc step", "text", "safe_pc_open_browser", "jarvis_chat_model", "jarvis:chat8b",
        ("pc_open_browser",), ("action_worker_agent",), "light", False, False, True, False,
        "local_terminal_session", True))
    payload = build_swarm_observability_read_model(route, detect_swarm_conflicts((route,)))

    assert payload["active_agents"] == ("action_worker_agent",)
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_tools"] == ("pc_open_browser",)
    assert payload["heavy_gpu_lock_status"] == "unlocked"
    assert payload["direct_execution_disabled_for_swarm"] is True
    assert payload["safe_action_delegated_to_action_library"] is True
    assert payload["delegated_execution_surface"] == "action_library"
