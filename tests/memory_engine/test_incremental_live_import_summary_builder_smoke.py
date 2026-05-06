from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_summary_builder import (
    build_incremental_live_import_summary,
)


def test_incremental_live_import_summary_builder_smoke() -> None:
    summary = build_incremental_live_import_summary(
        import_root_path="runtime_imports/chatgpt_export_01",
        write_root_path="runtime_history_store",
    )
    assert summary["incremental_ready"] is True
