from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.queue_models import (
    QueuePolicyContract,
    QueuePolicyRule,
)


def build_queue_policy_contract() -> QueuePolicyContract:
    """Build unified queue policy contract."""

    rules = (
        QueuePolicyRule(
            queue_type="critical_queue",
            max_items=32,
            overflow_action="reject_noncritical",
        ),
        QueuePolicyRule(
            queue_type="high_queue",
            max_items=64,
            overflow_action="throttle",
        ),
        QueuePolicyRule(
            queue_type="normal_queue",
            max_items=128,
            overflow_action="delay",
        ),
        QueuePolicyRule(
            queue_type="background_queue",
            max_items=256,
            overflow_action="pause_background",
        ),
        QueuePolicyRule(
            queue_type="deferred_queue",
            max_items=512,
            overflow_action="reschedule",
        ),
    )

    return QueuePolicyContract(
        total_rules=len(rules),
        rules=rules,
    )
