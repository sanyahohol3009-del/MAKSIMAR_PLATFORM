from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.self_readability import (
    build_jarvis_memory_self_read_preview,
    build_jarvis_memory_source_usage_pack,
)


def test_jarvis_memory_source_usage_preview_smoke() -> None:
    pack = build_jarvis_memory_source_usage_pack()
    preview = build_jarvis_memory_self_read_preview()

    assert pack.source_usage_pack_ready is True
    assert pack.total_sources == 3
    assert preview["preview_ready"] is True
    assert len(preview["sources_used"]) == 3
    assert preview["can_explain_sources_used"] is True
