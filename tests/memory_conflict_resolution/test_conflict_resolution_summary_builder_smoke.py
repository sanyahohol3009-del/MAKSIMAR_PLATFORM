from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_resolution_summary,
)


def test_conflict_resolution_summary_builder_smoke() -> None:
    summary = build_conflict_resolution_summary()

    assert summary["summary_ready"] is True
    assert summary["conflict_binding_entries"] == 2
    assert summary["conflict_ready_bindings"] == 2
    assert summary["approval_required_bindings"] == 2
    assert summary["approval_granted_bindings"] == 2
    assert summary["resolved_bindings"] == 2
