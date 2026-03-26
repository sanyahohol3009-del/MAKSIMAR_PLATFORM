from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_flow_map_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.flow_view_models import (
    ServerFlowViewContract,
    ServerFlowViewEntry,
)


def build_server_flow_view_contract() -> ServerFlowViewContract:
    """Build unified server-side flow view contract."""
    flow_map = build_flow_map_contract()

    steps = tuple(
        ServerFlowViewEntry(
            step_order=step.step_order,
            source_component=step.source_component,
            target_component=step.target_component,
            flow_name=step.flow_name,
            source_contract_bound=True,
        )
        for step in flow_map.steps
    )

    return ServerFlowViewContract(
        total_steps=len(steps),
        steps=steps,
    )
