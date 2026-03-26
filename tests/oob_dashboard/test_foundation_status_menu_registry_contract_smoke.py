from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_menu_registry_contract import (
    build_foundation_status_menu_registry_contract,
)


def test_foundation_status_menu_registry_contract_counts() -> None:
    """Foundation status menu registry contract should expose expected counts."""
    contract = build_foundation_status_menu_registry_contract()

    assert contract.total_entries == 4
    assert contract.left_menu_entries == 4
    assert contract.oob_visible_entries == 4
    assert contract.main_dashboard_visible_entries == 4
    assert contract.read_only_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_status_menu_registry_contract_runtime_entry() -> None:
    """Foundation status menu registry contract should expose runtime entry."""
    contract = build_foundation_status_menu_registry_contract()
    entry = contract.entries[0]

    assert entry.registry_entry_id == "foundationmenuregistry_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.menu_item_id == "menu_foundation_runtime_001"
    assert entry.menu_section == "foundation_core"
    assert entry.menu_order_index == 1
    assert entry.menu_label == "Runtime Core"
    assert entry.short_status_label == "RUNTIME"
    assert entry.visual_role == "central_core"
    assert entry.show_in_left_menu is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.startup_stage_index == 1


def test_foundation_status_menu_registry_contract_kernel_entry() -> None:
    """Foundation status menu registry contract should expose kernel entry."""
    contract = build_foundation_status_menu_registry_contract()
    entry = contract.entries[-1]

    assert entry.registry_entry_id == "foundationmenuregistry_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.menu_item_id == "menu_foundation_kernel_guard_001"
    assert entry.menu_section == "foundation_safety"
    assert entry.menu_order_index == 4
    assert entry.menu_label == "Kernel Watchdog"
    assert entry.short_status_label == "KERNEL"
    assert entry.visual_role == "outer_guard_ring"
    assert entry.show_in_left_menu is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True
    assert entry.operator_actions_allowed is False
    assert entry.startup_stage_index == 4


def test_foundation_status_menu_registry_contract_preserves_order() -> None:
    """Foundation status menu registry contract should preserve menu order."""
    contract = build_foundation_status_menu_registry_contract()

    assert [entry.menu_order_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.menu_item_id for entry in contract.entries] == [
        "menu_foundation_runtime_001",
        "menu_foundation_guard_001",
        "menu_foundation_core_guard_001",
        "menu_foundation_kernel_guard_001",
    ]
    assert [entry.menu_section for entry in contract.entries] == [
        "foundation_core",
        "foundation_safety",
        "foundation_safety",
        "foundation_safety",
    ]
