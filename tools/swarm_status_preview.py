from __future__ import annotations

import json

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_observability_runtime import (
    build_swarm_observability_read_model,
)
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import build_owner_identity_claim_for_terminal


def build_swarm_status_preview() -> dict[str, object]:
    route = route_swarm_task(
        "Джарвис, pytest упал, проверь ошибку",
        input_channel="text",
        owner_identity_claim=build_owner_identity_claim_for_terminal(),
    )
    conflict_report = detect_swarm_conflicts((route,))
    return build_swarm_observability_read_model(route, conflict_report)


def main() -> int:
    print(json.dumps(build_swarm_status_preview(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
