from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_context_reader import (
    build_jarvis_history_context,
)


def test_jarvis_history_context_reader_smoke() -> None:
    context = build_jarvis_history_context()

    assert context.memory_ids[0] == "ARCH-0001"
    assert context.context_ready is True
