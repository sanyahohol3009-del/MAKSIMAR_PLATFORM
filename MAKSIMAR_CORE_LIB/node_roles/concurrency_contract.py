from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.concurrency_models import (
    ConcurrencyContract,
    ConcurrencyRule,
)


def build_concurrency_contract() -> ConcurrencyContract:
    """Build unified concurrency guard contract."""

    rules = (
        ConcurrencyRule(
            resource_type="core_write",
            single_writer=True,
            max_parallel_tasks=1,
        ),
        ConcurrencyRule(
            resource_type="simulation_engine",
            single_writer=False,
            max_parallel_tasks=2,
        ),
        ConcurrencyRule(
            resource_type="ai_inference",
            single_writer=False,
            max_parallel_tasks=4,
        ),
    )

    return ConcurrencyContract(
        total_rules=len(rules),
        rules=rules,
    )
