from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_visual_composition_contract import (
    build_foundation_visual_composition_contract,
)


def test_foundation_visual_composition_contract_counts() -> None:
    """Foundation visual composition contract should expose expected counts."""
    contract = build_foundation_visual_composition_contract()

    assert contract.total_entries == 4
    assert contract.central_core_entries == 1
    assert contract.inner_guard_entries == 2
    assert contract.outer_guard_entries == 1
    assert contract.signal_visible_entries == 4
    assert contract.execution_stage_visible_entries == 4
    assert contract.startup_order_valid_entries == 4


def test_foundation_visual_composition_contract_runtime_entry() -> None:
    """Foundation visual composition contract should expose runtime center entry."""
    contract = build_foundation_visual_composition_contract()
    entry = contract.entries[0]

    assert entry.composition_entry_id == "foundationvisual_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.display_title == "Runtime Core"
    assert entry.visual_layer == "central_core"
    assert entry.visual_anchor == "center"
    assert entry.startup_stage_index == 1
    assert entry.central_to_core_map is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True


def test_foundation_visual_composition_contract_kernel_entry() -> None:
    """Foundation visual composition contract should expose kernel outer ring entry."""
    contract = build_foundation_visual_composition_contract()
    entry = contract.entries[-1]

    assert entry.composition_entry_id == "foundationvisual_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.visual_layer == "outer_guard_ring"
    assert entry.visual_anchor == "ring_outer_top"
    assert entry.startup_stage_index == 4
    assert entry.central_to_core_map is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.show_in_oob_dashboard is True
    assert entry.show_in_main_dashboard is True
    assert entry.read_only is True


def test_foundation_visual_composition_contract_preserves_visual_structure() -> None:
    """Foundation visual composition contract should preserve expected layout."""
    contract = build_foundation_visual_composition_contract()

    assert [entry.startup_stage_index for entry in contract.entries] == [1, 2, 3, 4]
    assert [entry.visual_layer for entry in contract.entries] == [
        "central_core",
        "inner_guard_ring",
        "inner_guard_ring",
        "outer_guard_ring",
    ]
    assert [entry.visual_anchor for entry in contract.entries] == [
        "center",
        "ring_inner_top",
        "ring_inner_right",
        "ring_outer_top",
    ]
