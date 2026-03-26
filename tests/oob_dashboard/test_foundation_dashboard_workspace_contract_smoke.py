from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_dashboard_workspace_contract import (
    build_foundation_dashboard_workspace_contract,
)


def test_foundation_dashboard_workspace_contract_counts() -> None:
    """Foundation dashboard workspace contract should expose expected counts."""
    contract = build_foundation_dashboard_workspace_contract()

    assert contract.workspace_id == "workspace_foundation_dashboard_001"
    assert contract.workspace_title == "Foundation Dashboard Workspace"
    assert contract.total_entries == 4
    assert contract.left_menu_entries == 4
    assert contract.center_core_entries == 1
    assert contract.inner_ring_entries == 2
    assert contract.outer_ring_entries == 1
    assert contract.signal_visible_entries == 4
    assert contract.execution_stage_visible_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_dashboard_workspace_contract_runtime_entry() -> None:
    """Foundation dashboard workspace contract should expose runtime entry."""
    contract = build_foundation_dashboard_workspace_contract()
    entry = contract.entries[0]

    assert entry.workspace_entry_id == "foundationworkspace_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.zone_id == "center_core"
    assert entry.zone_order_index == 2
    assert entry.panel_order_index == 1
    assert entry.display_title == "Runtime Core"
    assert entry.startup_stage_index == 1
    assert entry.left_menu_visible is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.workspace_mode == "oob_read_only"
    assert entry.read_only is True


def test_foundation_dashboard_workspace_contract_kernel_entry() -> None:
    """Foundation dashboard workspace contract should expose kernel entry."""
    contract = build_foundation_dashboard_workspace_contract()
    entry = contract.entries[-1]

    assert entry.workspace_entry_id == "foundationworkspace_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.zone_id == "outer_ring"
    assert entry.zone_order_index == 4
    assert entry.panel_order_index == 4
    assert entry.display_title == "Kernel Watchdog"
    assert entry.startup_stage_index == 4
    assert entry.left_menu_visible is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.workspace_mode == "oob_read_only"
    assert entry.read_only is True


def test_foundation_dashboard_workspace_contract_preserves_zone_order() -> None:
    """Foundation dashboard workspace contract should preserve expected zone order."""
    contract = build_foundation_dashboard_workspace_contract()

    assert [entry.startup_stage_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.zone_id for entry in contract.entries] == [
        "center_core",
        "inner_ring",
        "inner_ring",
        "outer_ring",
    ]
    assert [entry.panel_order_index for entry in contract.entries] == [1, 2, 3, 4]
