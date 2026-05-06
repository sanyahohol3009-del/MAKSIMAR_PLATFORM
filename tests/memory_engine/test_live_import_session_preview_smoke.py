from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session_preview,
)


def test_live_import_session_preview_smoke() -> None:
    preview = build_live_import_session_preview(
        "runtime_imports/chatgpt_export_01",
    )
    assert preview["whole_file_ready"] is True
