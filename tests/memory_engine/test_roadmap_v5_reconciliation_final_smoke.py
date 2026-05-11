from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_drift_preview
from MAKSIMAR_CORE_LIB.memory_engine.self_readability import build_jarvis_memory_self_read_preview
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_read_only_routing_integration_preview,
)


def test_roadmap_v5_reconciliation_final_smoke() -> None:
    drift = build_memory_drift_preview()
    self_read = build_jarvis_memory_self_read_preview()
    mempalace = build_mempalace_read_only_routing_integration_preview()

    assert drift["preview_ready"] is True
    assert drift["canonical_truth_change_allowed"] is False
    assert drift["auto_resolution_allowed"] is False

    assert self_read["preview_ready"] is True
    assert self_read["can_explain_where_searched"] is True
    assert self_read["can_explain_sources_used"] is True
    assert self_read["can_explain_constraints_applied"] is True
    assert self_read["can_explain_evidence_pack"] is True
    assert self_read["can_explain_preview_trace"] is True
    assert self_read["canonical_write_allowed"] is False
    assert self_read["runtime_mutation_allowed"] is False

    assert mempalace["routing_integration_ready"] is True
    assert mempalace["read_only_routing_enabled"] is True
    assert mempalace["subordinate_backend"] is True
    assert mempalace["write_routing_enabled"] is False
    assert mempalace["canonical_write_allowed"] is False
    assert mempalace["runtime_mutation_allowed"] is False
