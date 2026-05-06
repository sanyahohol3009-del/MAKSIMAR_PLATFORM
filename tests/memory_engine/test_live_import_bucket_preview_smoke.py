from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_bucket_builder import (
    build_live_import_bucket_preview,
)


def test_live_import_bucket_preview_smoke() -> None:
    preview = build_live_import_bucket_preview(
        "runtime_imports/chatgpt_export_01/conversations.json",
    )
    assert preview["bucket_count"] >= 1
