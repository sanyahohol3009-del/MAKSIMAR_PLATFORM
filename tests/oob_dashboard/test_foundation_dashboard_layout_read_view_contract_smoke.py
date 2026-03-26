from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_dashboard_layout_read_view_contract import (
    build_foundation_dashboard_layout_read_view_contract,
)


def test_foundation_dashboard_layout_read_view_contract_counts() -> None:
    """Foundation dashboard layout read-view contract should expose expected counts."""
    contract = build_foundation_dashboard_layout_read_view_contract()

    assert contract.total_entries == 4
    assert contract.left_menu_entries == 4
    assert contract.center_zone_entries == 1
    assert contract.ring_zone_entries == 3
    assert contract.signal_visible_entries == 4
    assert contract.execution_stage_visible_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_dashboard_layout_read_view_contract_runtime_entry() -> None:
    """Foundation dashboard layout read-view contract should expose runtime center entry."""
    contract = build_foundation_dashboard_layout_read_view_contract()
    entry = contract.entries[0]

    assert entry.layout_entry_id == "foundationlayout_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.display_title == "Runtime Core"
    assert entry.layout_zone == "center_core"
    assert entry.layout_order_index == 1
    assert entry.startup_stage_index == 1
    assert entry.left_menu_visible is True
    assert entry.center_visible is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.view_mode == "oob_read_only"
    assert entry.read_only is True


def test_foundation_dashboard_layout_read_view_contract_kernel_entry() -> None:
    """Foundation dashboard layout read-view contract should expose outer ring entry."""
    contract = build_foundation_dashboard_layout_read_view_contract()
    entry = contract.entries[-1]

    assert entry.layout_entry_id == "foundationlayout_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.layout_zone == "outer_ring"
    assert entry.layout_order_index == 4
    assert entry.startup_stage_index == 4
    assert entry.left_menu_visible is True
    assert entry.center_visible is False
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.view_mode == "oob_read_only"
    assert entry.read_only is True


def test_foundation_dashboard_layout_read_view_contract_preserves_layout_order() -> None:
    """Foundation dashboard layout read-view contract should preserve expected order."""
    contract = build_foundation_dashboard_layout_read_view_contract()

    assert [entry.layout_order_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.layout_zone for entry in contract.entries] == [
        "center_core",
        "inner_ring",
        "inner_ring",
        "outer_ring",
    ]
    assert [entry.startup_stage_index for entry in contract.entries] == [1, 2, 3, 4]
