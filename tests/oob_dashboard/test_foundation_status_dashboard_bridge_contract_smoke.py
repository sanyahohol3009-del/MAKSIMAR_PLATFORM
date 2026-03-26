from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_dashboard_bridge_contract import (
    build_foundation_status_dashboard_bridge_contract,
)


def test_foundation_status_dashboard_bridge_contract_counts() -> None:
    """Foundation status dashboard bridge contract should expose expected counts."""
    contract = build_foundation_status_dashboard_bridge_contract()

    assert contract.total_entries == 4
    assert contract.read_only_entries == 4
    assert contract.oob_visible_entries == 4
    assert contract.main_dashboard_visible_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_status_dashboard_bridge_contract_runtime_entry() -> None:
    """Foundation status dashboard bridge contract should expose runtime entry."""
    contract = build_foundation_status_dashboard_bridge_contract()
    entry = contract.entries[0]

    assert entry.bridge_entry_id == "foundationbridge_runtime_001"
    assert entry.status_surface_id == "statussurface_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.menu_label == "Foundation Runtime"
    assert entry.linked_session_name == "maksimar"
    assert entry.status_command == "./tools/ctl status"
    assert entry.truth_scope == "runtime"
    assert entry.startup_stage_index == 1
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.status_surface_contract_id == "STATUS_SURFACE_CONTRACT_v1"


def test_foundation_status_dashboard_bridge_contract_kernel_entry() -> None:
    """Foundation status dashboard bridge contract should expose kernel entry."""
    contract = build_foundation_status_dashboard_bridge_contract()
    entry = contract.entries[-1]

    assert entry.bridge_entry_id == "foundationbridge_kernel_guard_001"
    assert entry.status_surface_id == "statussurface_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.menu_label == "Foundation Kernel Watchdog"
    assert entry.linked_session_name == "maksimar_kernel_guard"
    assert entry.status_command == "./tools/kernel_guard_ctl status"
    assert entry.truth_scope == "kernel_guard"
    assert entry.startup_stage_index == 4
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.status_surface_contract_id == "STATUS_SURFACE_CONTRACT_v1"


def test_foundation_status_dashboard_bridge_contract_preserves_order() -> None:
    """Foundation status dashboard bridge contract should preserve startup order."""
    contract = build_foundation_status_dashboard_bridge_contract()

    assert [entry.startup_stage_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
