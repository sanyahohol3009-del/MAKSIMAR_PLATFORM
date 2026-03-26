from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.priority_models import (
    TaskPriorityContract,
    TaskPriorityRule,
)


def build_task_priority_contract() -> TaskPriorityContract:
    """Build unified task priority contract."""

    rules = (
        TaskPriorityRule(task_type="safety_check", priority="critical"),
        TaskPriorityRule(task_type="user_query", priority="high"),
        TaskPriorityRule(task_type="automation_task", priority="normal"),
        TaskPriorityRule(task_type="indexing_task", priority="background"),
        TaskPriorityRule(task_type="bulk_reindex", priority="deferred"),
    )

    return TaskPriorityContract(
        total_rules=len(rules),
        rules=rules,
    )
