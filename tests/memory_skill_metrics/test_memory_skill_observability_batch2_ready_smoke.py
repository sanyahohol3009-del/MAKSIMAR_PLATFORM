from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_adapter_selection_metrics_contract,
    build_memory_promotion_metrics_contract,
    build_memory_skill_preview,
)


def test_memory_skill_observability_batch2_ready_smoke() -> None:
    promotion = build_memory_promotion_metrics_contract()
    adapter = build_memory_adapter_selection_metrics_contract()
    preview = build_memory_skill_preview()

    assert promotion.ready_entries == promotion.total_entries
    assert adapter.ready_entries == adapter.total_entries
    assert preview["phase_batch_ready"] is True
