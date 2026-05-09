from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_preview,
)


def test_memory_skill_preview_builder_smoke() -> None:
    preview = build_memory_skill_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert preview["flow"] == (
        "memory_skill_base_metrics",
        "memory_retrieval_metrics",
        "memory_conflict_metrics",
        "memory_promotion_metrics",
        "memory_adapter_selection_metrics",
        "memory_skill_summary",
        "memory_skill_preview",
    )
