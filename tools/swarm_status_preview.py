from __future__ import annotations

import json

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_observability_runtime import (
    build_swarm_observability_read_model,
)
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract


def build_swarm_status_preview() -> dict[str, object]:
    route = route_swarm_task(
        SwarmTaskContract(
            task_id="swarm_status_preview", user_text="typed task from Semantic Spine", input_channel="text",
            normalized_intent="code_debug", selected_model_role_id="coder_model",
            selected_model_id="jarvis:coder7b", selected_tools=("pytest_report_read",),
            candidate_agent_roles=("project_coder_agent",), task_complexity="medium",
            heavy_model_requested=False, risk_gate_required=False,
            safe_direct_action_candidate=False, read_only_discovery_only=True,
            owner_identity_source="local_terminal_session", direct_execution_requested=False,
        ),
    )
    conflict_report = detect_swarm_conflicts((route,))
    return build_swarm_observability_read_model(route, conflict_report)


def main() -> int:
    print(json.dumps(build_swarm_status_preview(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
