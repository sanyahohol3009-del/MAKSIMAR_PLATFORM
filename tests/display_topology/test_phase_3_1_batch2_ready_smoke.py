from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_assignment_binding_contract,
    build_display_capability_binding_contract,
    build_display_registry_contract,
    build_display_role_binding_contract,
    build_display_topology_preview,
    build_display_topology_summary,
    build_zone_layout_contract,
)


def test_phase_3_1_batch2_ready_smoke() -> None:
    display_registry = build_display_registry_contract()
    roles = build_display_role_binding_contract()
    zones = build_zone_layout_contract()
    capabilities = build_display_capability_binding_contract()
    assignments = build_display_assignment_binding_contract()
    summary = build_display_topology_summary()
    preview = build_display_topology_preview()

    assert display_registry.ready_entries == display_registry.total_entries
    assert roles.ready_roles == roles.total_roles
    assert zones.ready_zones == zones.total_zones
    assert capabilities.ready_capabilities == capabilities.total_capabilities
    assert assignments.ready_assignments == assignments.total_assignments
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["direct_switching_allowed"] == 0
