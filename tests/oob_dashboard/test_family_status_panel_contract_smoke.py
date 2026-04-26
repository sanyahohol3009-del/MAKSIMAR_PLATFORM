from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.family_status_panel_contract import (
    build_family_status_panel_contract,
)


def test_family_status_panel_contract_builds() -> None:
    contract = build_family_status_panel_contract()

    assert contract.panel_id == "panel_family_status"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_family_status_panel_contract_contains_expected_entries() -> None:
    contract = build_family_status_panel_contract()

    states = tuple(
        (entry.family_member_id, entry.family_role, entry.family_state)
        for entry in contract.entries
    )

    assert states == (
        ("family_guardian_primary", "guardian", "active_guardian_context"),
        ("family_child_monitoring", "child_monitoring", "protected_monitoring_context"),
        ("family_assistant_core", "assistant", "family_safe_mode"),
    )
