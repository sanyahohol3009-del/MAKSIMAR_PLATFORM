from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_read_model_contract import (
    build_foundation_status_read_model_contract,
)


def test_foundation_status_read_model_contract_counts() -> None:
    """Foundation status read model contract should expose expected counts."""
    contract = build_foundation_status_read_model_contract()

    assert contract.total_entries == 4
    assert contract.central_core_entries == 1
    assert contract.guard_ring_entries == 3
    assert contract.signal_visible_entries == 4
    assert contract.execution_stage_visible_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_status_read_model_contract_runtime_entry() -> None:
    """Foundation status read model contract should expose runtime core entry."""
    contract = build_foundation_status_read_model_contract()
    entry = contract.entries[0]

    assert entry.read_model_entry_id == "foundationreadmodel_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.menu_section == "foundation_core"
    assert entry.menu_order_index == 1
    assert entry.display_title == "Runtime Core"
    assert entry.visual_role == "central_core"
    assert entry.truth_scope == "runtime"
    assert entry.startup_stage_index == 1
    assert entry.source_session_name == "maksimar"
    assert entry.source_status_command == "./tools/ctl status"
    assert entry.read_only is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.central_to_core_map is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True


def test_foundation_status_read_model_contract_kernel_entry() -> None:
    """Foundation status read model contract should expose kernel watchdog entry."""
    contract = build_foundation_status_read_model_contract()
    entry = contract.entries[-1]

    assert entry.read_model_entry_id == "foundationreadmodel_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.menu_section == "foundation_safety"
    assert entry.menu_order_index == 4
    assert entry.display_title == "Kernel Watchdog"
    assert entry.visual_role == "outer_guard_ring"
    assert entry.truth_scope == "kernel_guard"
    assert entry.startup_stage_index == 4
    assert entry.source_session_name == "maksimar_kernel_guard"
    assert entry.source_status_command == "./tools/kernel_guard_ctl status"
    assert entry.read_only is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.central_to_core_map is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True


def test_foundation_status_read_model_contract_preserves_visual_order() -> None:
    """Foundation status read model contract should preserve expected visual order."""
    contract = build_foundation_status_read_model_contract()

    assert [entry.menu_order_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
    assert [entry.visual_role for entry in contract.entries] == [
        "central_core",
        "inner_guard_ring",
        "inner_guard_ring",
        "outer_guard_ring",
    ]
