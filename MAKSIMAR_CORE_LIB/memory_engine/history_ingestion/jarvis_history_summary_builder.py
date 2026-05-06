from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_context_reader import (
    build_jarvis_history_context,
)


def build_jarvis_history_summary() -> Dict[str, object]:
    context = build_jarvis_history_context()
    return {
        "memory_count": len(context.memory_ids),
        "first_memory_id": context.memory_ids[0],
        "first_title": context.titles[0],
        "readable_by_jarvis": context.readable_by_jarvis,
        "context_ready": context.context_ready,
    }
