from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_id_models import (
    MemoryIdPrefix,
    MemoryObjectId,
)


def build_memory_object_id(
    prefix: MemoryIdPrefix,
    numeric_id: int,
) -> MemoryObjectId:
    return MemoryObjectId(
        prefix=prefix,
        numeric_id=numeric_id,
        value=f"{prefix}-{numeric_id:04d}",
    )


def build_memory_identity_preview() -> Dict[str, object]:
    arch = build_memory_object_id("ARCH", 1)
    inc = build_memory_object_id("INC", 4)
    roadmap = build_memory_object_id("ROADMAP", 12)

    return {
        "architecture_id": arch.value,
        "incident_id": inc.value,
        "roadmap_id": roadmap.value,
        "identity_ready": True,
    }
