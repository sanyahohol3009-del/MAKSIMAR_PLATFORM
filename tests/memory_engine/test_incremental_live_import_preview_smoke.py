from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_builder import (
    build_incremental_live_import_preview,
)


def test_incremental_live_import_preview_smoke() -> None:
    preview = build_incremental_live_import_preview(
        import_root_path="runtime_imports/chatgpt_export_01",
        write_root_path="runtime_history_store",
    )
    assert preview["existing_conversations"] == 18
