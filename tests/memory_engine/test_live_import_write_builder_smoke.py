from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_builder import (
    build_live_import_write_plan,
)


def test_live_import_write_builder_smoke() -> None:
    plan = build_live_import_write_plan(
        "runtime_imports/chatgpt_export_01",
    )
    assert plan["session"]["session_id"] == "LIVE-IMPORT-CHATGPT-0001"
