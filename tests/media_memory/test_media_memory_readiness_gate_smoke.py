from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)


def test_media_memory_readiness_gate_smoke() -> None:
    readiness = build_media_memory_phase_readiness()

    assert readiness.phase_core_ready is True
    assert readiness.preview_ready is True
    assert readiness.media_memory_ready is True
    assert readiness.storage_binding_ready is True
    assert readiness.no_binary_payloads is True
