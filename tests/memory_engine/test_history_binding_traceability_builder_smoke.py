from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_traceability_projection,
)


def test_history_binding_traceability_builder_smoke() -> None:
    payload = build_history_binding_traceability_projection()

    assert payload["memory_id"]
    assert payload["source_ref"]
    assert isinstance(payload["affected_files"], tuple)
    assert payload["timeline_id"]
    assert payload["traceability_ready"] is True
