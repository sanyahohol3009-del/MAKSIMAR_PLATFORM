from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_id_allocator import (
    build_memory_identity_preview,
    build_memory_object_id,
)


def test_memory_id_allocator_smoke() -> None:
    arch_id = build_memory_object_id("ARCH", 1)
    inc_id = build_memory_object_id("INC", 4)

    assert arch_id.value == "ARCH-0001"
    assert inc_id.value == "INC-0004"


def test_memory_identity_preview_smoke() -> None:
    preview = build_memory_identity_preview()
    assert preview["architecture_id"] == "ARCH-0001"
    assert preview["incident_id"] == "INC-0004"
    assert preview["roadmap_id"] == "ROADMAP-0012"
    assert preview["identity_ready"] is True
