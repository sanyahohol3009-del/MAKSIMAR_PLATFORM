from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_bucket_builder import (
    build_live_import_conversation_buckets,
)


def test_live_import_conversation_bucket_builder_smoke() -> None:
    buckets = build_live_import_conversation_buckets(
        "runtime_imports/chatgpt_export_01/conversations.json",
    )
    assert len(buckets) >= 1
