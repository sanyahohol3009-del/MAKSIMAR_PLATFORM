from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_promotion_metrics_contract,
)


def test_memory_promotion_metrics_models_smoke() -> None:
    contract = build_memory_promotion_metrics_contract()

    assert contract.total_entries == 3
    assert contract.ready_entries == contract.total_entries
    assert contract.auto_promotion_allowed_entries == 0
    assert contract.approval_required_entries == contract.total_entries
    assert contract.conflict_clear_entries == contract.total_entries
    assert contract.citation_ready_entries == contract.total_entries
    assert contract.read_only_entries == contract.total_entries
