from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.memory_source_priority_models import (
    build_memory_source_priority_policy,
)


def test_memory_source_priority_models_smoke() -> None:
    policy = build_memory_source_priority_policy()

    assert policy.source_priority_ready is True
    assert policy.unique_priority_orders is True
    assert policy.subordinate_backend_lowest_priority is True
    assert policy.evidence_required_for_all_sources is True
    assert policy.no_source_can_override_higher_priority is True
