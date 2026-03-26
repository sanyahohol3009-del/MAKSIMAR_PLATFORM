from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_contract,
)


def test_display_topology_contract_builds() -> None:
    """Display topology contract should build successfully."""
    contract = build_display_topology_contract()

    assert contract.total_displays == 3
    assert contract.private_displays == 1
    assert contract.shared_displays == 2
    assert contract.multilingual_ready_displays == 3


def test_display_topology_contract_contains_expected_display_roles() -> None:
    """Display topology contract should expose expected display roles."""
    contract = build_display_topology_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.display_id == "display_primary_dashboard_001"
    assert first.display_role == "primary_dashboard_display"
    assert first.default_panel_ids == (
        "panel_monitoring_panel",
        "panel_memory_project_architecture",
    )

    assert second.display_id == "display_engineering_001"
    assert second.display_role == "engineering_display"
    assert second.default_panel_ids == ("panel_simulation_skill_overview",)

    assert last.display_id == "display_mobile_proxy_001"
    assert last.display_role == "mobile_display_proxy"
    assert last.default_panel_ids == ("panel_memory_project_architecture",)


def test_display_topology_contract_preserves_expected_capabilities() -> None:
    """Display topology contract should preserve expected capability bindings."""
    contract = build_display_topology_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert "multi_window" in first.capabilities
    assert first.visibility_mode == "shared"

    assert "spatial_overlay" in second.capabilities
    assert second.visibility_mode == "shared"

    assert "mobile_proxy" in last.capabilities
    assert "private_display" in last.capabilities
    assert last.visibility_mode == "private"
