from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_builder import (
    build_live_import_write_preview,
)


def test_live_import_write_preview_smoke() -> None:
    preview = build_live_import_write_preview(
        "runtime_imports/chatgpt_export_01",
    )
    assert preview["write_ready"] is True
