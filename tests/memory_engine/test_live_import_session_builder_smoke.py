from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session,
)


def test_live_import_session_builder_smoke() -> None:
    session = build_live_import_session(
        "runtime_imports/chatgpt_export_01",
    )
    assert session.by_conversation_ready is True
