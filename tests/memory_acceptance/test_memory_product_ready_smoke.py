from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import (
    build_memory_readiness_summary,
    build_memory_release_preview,
)


def test_memory_product_ready_smoke() -> None:
    summary = build_memory_readiness_summary()
    preview = build_memory_release_preview()

    assert summary["readiness_ready"] is True
    assert preview["memory_product_ready"] is True
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["release_allowed_without_operator_approval"] is False
