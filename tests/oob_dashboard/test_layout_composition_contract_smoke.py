from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_layout_composition_contract,
)


def test_layout_composition_contract_builds() -> None:
    """Layout composition contract should build successfully."""
    contract = build_layout_composition_contract()

    assert contract.total_entries == 19
    assert contract.foundation_monitoring_entries == 8
    assert contract.operator_surface_entries == 3
    assert contract.expansion_surface_entries == 8


def test_layout_composition_chat_entry() -> None:
    """Chat panel should occupy the primary operator main slot."""
    contract = build_layout_composition_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.workspace_id == "workspace_operator_main"
    assert entry.layout_zone == "main_focus"
    assert entry.layout_slot == "slot_main_1"
    assert entry.display_target_id == "display_primary_operator"


def test_layout_composition_foundation_runtime_entry() -> None:
    """Foundation runtime panel should occupy the monitoring main slot."""
    contract = build_layout_composition_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.workspace_id == "workspace_foundation_monitoring"
    assert entry.layout_zone == "main_focus"
    assert entry.layout_slot == "slot_main_1"
    assert entry.display_target_id == "display_secondary_diagnostics"


def test_layout_composition_navigation_entry() -> None:
    """Navigation panel should stay in expansion secondary slot."""
    contract = build_layout_composition_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.workspace_id == "workspace_expansion_observability"
    assert entry.layout_zone == "secondary_zone"
    assert entry.layout_slot == "slot_secondary_2"
    assert entry.display_target_id == "display_tertiary_expansion"
