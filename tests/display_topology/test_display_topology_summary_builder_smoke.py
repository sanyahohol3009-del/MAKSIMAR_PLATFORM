from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_display_topology_summary


def test_display_topology_summary_builder_smoke() -> None:
    summary = build_display_topology_summary()

    assert summary["summary_ready"] is True
    assert summary["display_topology_displays"] == 3
    assert summary["display_topology_private_displays"] == 1
    assert summary["display_topology_shared_displays"] == 2
    assert summary["display_topology_multilingual_ready_displays"] == 3
    assert summary["display_topology_explainable_displays"] == 3
    assert summary["display_topology_registry_routed_displays"] == 3
    assert summary["display_orchestration_entries"] == 3
    assert summary["dashboard_read_only_phase_ready"] is True
    assert summary["skill_domain_summary_ready"] is True
    assert summary["skill_domain_preview_ready"] is True
    assert summary["action_execution_allowed"] == 0
    assert summary["backend_execution_allowed"] == 0
