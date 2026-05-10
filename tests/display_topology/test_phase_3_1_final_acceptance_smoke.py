from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_assignment_binding_contract,
    build_display_capability_binding_contract,
    build_display_registry_contract,
    build_display_role_binding_contract,
    build_display_topology_phase_preview,
    build_display_topology_phase_readiness,
    build_display_topology_preview,
    build_display_topology_summary,
    build_zone_layout_contract,
)


def test_phase_3_1_final_acceptance_smoke() -> None:
    registry = build_display_registry_contract()
    roles = build_display_role_binding_contract()
    zones = build_zone_layout_contract()
    capabilities = build_display_capability_binding_contract()
    assignments = build_display_assignment_binding_contract()
    summary = build_display_topology_summary()
    preview = build_display_topology_preview()
    readiness = build_display_topology_phase_readiness()
    phase_preview = build_display_topology_phase_preview()

    assert registry.ready_entries == registry.total_entries
    assert registry.direct_switching_allowed_entries == 0

    assert roles.ready_roles == roles.total_roles
    assert roles.private_roles == 1
    assert roles.shared_roles == 2

    assert zones.ready_zones == zones.total_zones
    assert zones.read_only_zones == zones.total_zones

    assert capabilities.ready_capabilities == capabilities.total_capabilities
    assert capabilities.direct_execution_allowed_capabilities == 0

    assert assignments.ready_assignments == assignments.total_assignments
    assert assignments.direct_switching_allowed_assignments == 0

    assert summary["summary_ready"] is True
    assert summary["memory_views_display_bindable"] is True
    assert summary["action_execution_allowed"] == 0
    assert summary["backend_execution_allowed"] == 0
    assert summary["direct_switching_allowed"] == 0

    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True
