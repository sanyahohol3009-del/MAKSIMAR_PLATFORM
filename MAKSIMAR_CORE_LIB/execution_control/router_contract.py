from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.router_models import (
    ExecutionRoute,
    ExecutionRouterContract,
)


def build_execution_router_contract() -> ExecutionRouterContract:
    """Build unified execution router contract."""

    routes = (
        ExecutionRoute(
            request_id="req_001",
            worker_id="ai_worker",
            target_node="home_node",
            route_allowed=True,
        ),
        ExecutionRoute(
            request_id="req_002",
            worker_id="automation_worker",
            target_node="dev_node",
            route_allowed=False,
        ),
    )

    return ExecutionRouterContract(
        total_routes=len(routes),
        routes=routes,
    )
