from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.backpressure_models import (
    BackpressureContract,
    BackpressureRule,
)


def build_backpressure_contract() -> BackpressureContract:
    """Build unified backpressure contract."""

    rules = (
        BackpressureRule(
            trigger_name="cpu_pressure",
            action_name="delay_background_tasks",
            heavy_requests_blocked=False,
        ),
        BackpressureRule(
            trigger_name="queue_overflow",
            action_name="block_new_heavy_requests",
            heavy_requests_blocked=True,
        ),
        BackpressureRule(
            trigger_name="memory_pressure",
            action_name="enable_degraded_mode",
            heavy_requests_blocked=True,
        ),
    )

    return BackpressureContract(
        total_rules=len(rules),
        rules=rules,
    )
