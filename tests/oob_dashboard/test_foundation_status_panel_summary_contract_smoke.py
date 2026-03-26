from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_panel_summary_contract import (
    build_foundation_status_panel_summary_contract,
)


def test_foundation_status_panel_summary_contract_counts() -> None:
    """Foundation status panel summary contract should expose expected counts."""
    contract = build_foundation_status_panel_summary_contract()

    assert contract.total_entries == 4
    assert contract.left_menu_entries == 4
    assert contract.oob_visible_entries == 4
    assert contract.main_dashboard_visible_entries == 4
    assert contract.read_only_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_status_panel_summary_contract_runtime_entry() -> None:
    """Foundation status panel summary contract should expose runtime entry."""
    contract = build_foundation_status_panel_summary_contract()
    entry = contract.entries[0]

    assert entry.summary_entry_id == "foundationsummary_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.menu_section == "foundation_core"
    assert entry.menu_order_index == 1
    assert entry.display_title == "Runtime Core"
    assert entry.short_status_label == "RUNTIME"
    assert entry.visual_role == "central_core"
    assert entry.source_status_command == "./tools/ctl status"
    assert entry.source_session_name == "maksimar"
    assert entry.startup_stage_index == 1
    assert entry.show_in_left_menu is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True


def test_foundation_status_panel_summary_contract_kernel_entry() -> None:
    """Foundation status panel summary contract should expose kernel entry."""
    contract = build_foundation_status_panel_summary_contract()
    entry = contract.entries[-1]

    assert entry.summary_entry_id == "foundationsummary_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.menu_section == "foundation_safety"
    assert entry.menu_order_index == 4
    assert entry.display_title == "Kernel Watchdog"
    assert entry.short_status_label == "KERNEL"
    assert entry.visual_role == "outer_guard_ring"
    assert entry.source_status_command == "./tools/kernel_guard_ctl status"
    assert entry.source_session_name == "maksimar_kernel_guard"
    assert entry.startup_stage_index == 4
    assert entry.show_in_left_menu is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True


def test_foundation_status_panel_summary_contract_preserves_menu_order() -> None:
    """Foundation status panel summary contract should preserve expected menu order."""
    contract = build_foundation_status_panel_summary_contract()

    assert [entry.menu_order_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.menu_section for entry in contract.entries] == [
        "foundation_core",
        "foundation_safety",
        "foundation_safety",
        "foundation_safety",
    ]
    assert [entry.short_status_label for entry in contract.entries] == [
        "RUNTIME",
        "STOP-GATE",
        "CORE-GUARD",
        "KERNEL",
    ]
