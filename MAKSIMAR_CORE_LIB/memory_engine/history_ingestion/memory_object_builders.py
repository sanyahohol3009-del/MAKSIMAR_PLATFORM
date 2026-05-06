from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
    MemorySource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_validators import (
    validate_memory_object_minimum_required_fields,
)


def build_minimal_memory_object() -> MemoryObject:
    memory_object = MemoryObject(
        memory_id="ARCH-0001",
        memory_type="architecture_decision",
        title="Runtime truth path fixed",
        one_line_summary="Runtime truth path stabilized through guard-chain checkpoints.",
        status="validated",
        truth_level="validated_project_fact",
        project_area=("runtime", "truth_feed"),
        source=MemorySource(
            source_type="chat",
            source_ref="working_chat_memory_track_01",
            timestamp_utc="2026-05-04T00:00:00Z",
        ),
        affects=(
            "CORE_ROOT/core_guard.py",
            "CORE_ROOT/kernel_watchdog.py",
        ),
        next_step_id="PHASE3-BATCH1",
        next_step_summary="Start JARVIS memory truth/feed foundation mapping.",
        tags=("runtime", "truth", "checkpoint"),
    )
    validate_memory_object_minimum_required_fields(memory_object)
    return memory_object


def build_memory_object_preview(
    memory_object: MemoryObject,
) -> Dict[str, object]:
    validate_memory_object_minimum_required_fields(memory_object)
    return {
        "memory_id": memory_object.memory_id,
        "memory_type": memory_object.memory_type,
        "status": memory_object.status,
        "truth_level": memory_object.truth_level,
        "panel_ready": memory_object.panel_ready,
        "timeline_ready": memory_object.timeline_ready,
        "filter_ready": memory_object.filter_ready,
        "affects_count": len(memory_object.affects),
        "project_area_count": len(memory_object.project_area),
        "tag_count": len(memory_object.tags),
    }
