from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_builder import (
    build_incremental_live_import_result,
)


def test_incremental_live_import_detects_new_conversations_smoke() -> None:
    result = build_incremental_live_import_result(
        import_root_path="runtime_imports/chatgpt_export_01",
        write_root_path="runtime_history_store",
    )
    assert result.new_conversations == 0
