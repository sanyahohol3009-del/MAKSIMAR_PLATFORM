from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_assignment_binding_contract,
    build_display_capability_binding_contract,
    build_display_registry_contract,
    build_display_topology_summary,
)


def test_phase_3_1_no_direct_switching_smoke() -> None:
    registry = build_display_registry_contract()
    capabilities = build_display_capability_binding_contract()
    assignments = build_display_assignment_binding_contract()
    summary = build_display_topology_summary()

    assert registry.direct_switching_allowed_entries == 0
    assert capabilities.direct_execution_allowed_capabilities == 0
    assert assignments.direct_switching_allowed_assignments == 0
    assert summary["direct_switching_allowed"] == 0
