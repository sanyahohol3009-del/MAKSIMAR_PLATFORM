from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.version_control_panel_contract import (
    build_version_control_panel_contract,
)


def test_version_control_panel_contract_builds() -> None:
    contract = build_version_control_panel_contract()

    assert contract.panel_id == "panel_version_control_dashboard"
    assert contract.total_entries == 2
    assert contract.operator_visible is True


def test_version_control_panel_contract_contains_expected_states() -> None:
    contract = build_version_control_panel_contract()

    states = tuple((entry.sync_state, entry.branch_name) for entry in contract.entries)

    assert states == (
        ("pending_changes", "main"),
        ("clean", "main"),
    )
