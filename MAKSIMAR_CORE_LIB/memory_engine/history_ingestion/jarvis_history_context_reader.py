from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_read_models import (
    JarvisHistoryReadModel,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def build_jarvis_history_context() -> JarvisHistoryReadModel:
    memory_object = build_minimal_memory_object()
    return JarvisHistoryReadModel(
        memory_ids=(memory_object.memory_id,),
        titles=(memory_object.title,),
        readable_by_jarvis=True,
        context_ready=True,
    )


def build_jarvis_history_context_preview() -> Dict[str, object]:
    context = build_jarvis_history_context()
    return {
        "memory_count": len(context.memory_ids),
        "first_memory_id": context.memory_ids[0],
        "first_title": context.titles[0],
        "readable_by_jarvis": context.readable_by_jarvis,
        "context_ready": context.context_ready,
    }
