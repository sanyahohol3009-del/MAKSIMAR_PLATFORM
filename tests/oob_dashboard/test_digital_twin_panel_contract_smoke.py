from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.digital_twin_panel_contract import (
    build_digital_twin_panel_contract,
)


def test_digital_twin_panel_contract_builds() -> None:
    contract = build_digital_twin_panel_contract()

    assert contract.panel_id == "panel_digital_twin"
    assert contract.total_entries == 3
    assert contract.operator_visible is True


def test_digital_twin_panel_contract_contains_expected_entries() -> None:
    contract = build_digital_twin_panel_contract()

    states = tuple(
        (entry.twin_component_id, entry.twin_state, entry.sync_state)
        for entry in contract.entries
    )

    assert states == (
        ("surface_model", "ready", "in_sync"),
        ("toolpath_model", "ready", "in_sync"),
        ("material_profile", "ready", "in_sync"),
    )
