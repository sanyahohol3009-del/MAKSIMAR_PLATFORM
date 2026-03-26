from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map.flow_models import (
    FlowMapContract,
    FlowStep,
)


def build_flow_map_contract() -> FlowMapContract:
    """Build unified architecture flow map contract."""

    steps = (
        FlowStep(
            step_order=1,
            source_component="input_adapter",
            target_component="request_classifier",
            flow_name="user_input_flow",
        ),
        FlowStep(
            step_order=2,
            source_component="request_classifier",
            target_component="control_plane",
            flow_name="routing_flow",
        ),
        FlowStep(
            step_order=3,
            source_component="control_plane",
            target_component="execution_control",
            flow_name="execution_entry_flow",
        ),
        FlowStep(
            step_order=4,
            source_component="execution_control",
            target_component="workers",
            flow_name="worker_dispatch_flow",
        ),
        FlowStep(
            step_order=5,
            source_component="workers",
            target_component="oob_dashboard",
            flow_name="read_only_view_flow",
        ),
    )

    return FlowMapContract(
        total_steps=len(steps),
        steps=steps,
    )
