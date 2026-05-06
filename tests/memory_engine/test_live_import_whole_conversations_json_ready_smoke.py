from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_summary_builder import (
    build_live_import_summary,
)


def test_live_import_whole_conversations_json_ready_smoke() -> None:
    summary = build_live_import_summary(
        "runtime_imports/chatgpt_export_01",
    )
    assert summary["whole_file_ready"] is True
