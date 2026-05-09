from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_preview,
)


def test_storage_registry_preview_builder_smoke() -> None:
    preview = build_storage_registry_preview()

    assert preview["preview_ready"] is True
    assert preview["storage_ready_for_m2_nas"] is True
    assert preview["total_entries"] == len(preview["entries"])
    assert "retrieval_index" in preview["entry_kinds"]
    assert "model_store" in preview["entry_kinds"]
