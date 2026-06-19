from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmAgentHealthReadModel, SwarmStatusReadModel
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import SwarmConflictReport
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import SwarmTaskRoute


def build_swarm_observability_read_model(
    route: SwarmTaskRoute,
    conflict_report: SwarmConflictReport,
) -> dict[str, Any]:
    status = SwarmStatusReadModel(
        read_model_id="swarm_status_read_model_v1",
        active_agents=route.selected_agent_roles,
        selected_model_role=route.selected_model_role_id,
        selected_tools=route.selected_tools,
        conflict_status="blocked" if conflict_report.conflict_detected else "clear",
        heavy_gpu_lock_status=conflict_report.heavy_gpu_lock_status,
        direct_execution_disabled_for_swarm=True,
        safe_action_delegated_to_action_library=True,
    )
    health = tuple(
        SwarmAgentHealthReadModel(
            read_model_id=f"swarm_agent_health_{agent_role}_v1",
            agent_role=agent_role,
            status="active",
            selected_model_role=route.selected_model_role_id,
            heavy_gpu_candidate=route.heavy_model_requested,
            direct_execution_allowed=False,
        ).to_read_model()
        for agent_role in route.selected_agent_roles
    )
    payload = status.to_read_model()
    payload["agent_health"] = health
    payload["conflict"] = conflict_report.as_dict()
    payload["delegated_execution_surface"] = route.delegated_execution_surface
    payload["selected_model_id"] = route.selected_model_id
    return payload
