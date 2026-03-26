from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.workload_models import (
    WorkloadPlacementContract,
    WorkloadPlacementRule,
)


def build_workload_placement_contract() -> WorkloadPlacementContract:
    """Build unified workload placement matrix contract."""

    rules = (
        WorkloadPlacementRule(
            workload_type="ui_action",
            allowed_node_role="mobile_node",
            preferred=True,
        ),
        WorkloadPlacementRule(
            workload_type="chat_routing",
            allowed_node_role="dev_node",
            preferred=True,
        ),
        WorkloadPlacementRule(
            workload_type="automation_task",
            allowed_node_role="dev_node",
            preferred=False,
        ),
        WorkloadPlacementRule(
            workload_type="heavy_inference",
            allowed_node_role="home_node",
            preferred=True,
        ),
        WorkloadPlacementRule(
            workload_type="simulation_task",
            allowed_node_role="home_node",
            preferred=True,
        ),
    )

    return WorkloadPlacementContract(
        total_rules=len(rules),
        rules=rules,
    )
