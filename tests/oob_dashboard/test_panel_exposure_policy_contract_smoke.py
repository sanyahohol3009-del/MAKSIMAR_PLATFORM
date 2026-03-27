from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_exposure_policy_contract,
)


def test_panel_exposure_policy_contract_builds() -> None:
    """Panel exposure policy contract should build successfully."""
    contract = build_panel_exposure_policy_contract()

    assert contract.total_entries == 19
    assert contract.oob_only_entries == 0
    assert contract.main_dashboard_visible_entries == 9
    assert contract.shared_visible_entries == 9
    assert contract.hidden_internal_entries == 1


def test_panel_exposure_policy_chat_entry() -> None:
    """Chat panel should be main-dashboard-only and restricted."""
    contract = build_panel_exposure_policy_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.exposure_level == "main_dashboard_visible"
    assert entry.visibility_policy == "restricted_operator"
    assert entry.visible_in_oob_dashboard is False
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_navigation is True


def test_panel_exposure_policy_foundation_runtime_entry() -> None:
    """Foundation runtime panel should remain shared visible."""
    contract = build_panel_exposure_policy_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.exposure_level == "shared_visible"
    assert entry.visibility_policy == "read_only_public"
    assert entry.visible_in_oob_dashboard is True
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_navigation is True


def test_panel_exposure_policy_navigation_entry() -> None:
    """Navigation panel should stay hidden internal."""
    contract = build_panel_exposure_policy_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.exposure_level == "hidden_internal"
    assert entry.visibility_policy == "hidden_internal"
    assert entry.visible_in_oob_dashboard is False
    assert entry.visible_in_main_dashboard is False
    assert entry.visible_in_navigation is False
