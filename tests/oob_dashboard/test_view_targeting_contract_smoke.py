from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_view_targeting_contract,
)


def test_view_targeting_contract_builds() -> None:
    """View targeting contract should build successfully."""
    contract = build_view_targeting_contract()

    assert contract.total_entries == 19
    assert contract.foundation_views == 4
    assert contract.diagnostics_views == 4
    assert contract.interaction_views == 3
    assert contract.execution_views == 7
    assert contract.navigation_views == 1


def test_view_targeting_chat_entry() -> None:
    """Chat panel should map to canonical interaction view."""
    contract = build_view_targeting_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.view_id == "view_chat"
    assert entry.view_target_kind == "interaction_view"
    assert entry.view_scope == "interaction"


def test_view_targeting_foundation_runtime_entry() -> None:
    """Foundation runtime panel should map to canonical foundation view."""
    contract = build_view_targeting_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.view_id == "view_foundation_runtime"
    assert entry.view_target_kind == "foundation_view"
    assert entry.view_scope == "foundation"


def test_view_targeting_navigation_entry() -> None:
    """Navigation panel should map to canonical navigation view."""
    contract = build_view_targeting_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.view_id == "view_navigation"
    assert entry.view_target_kind == "navigation_view"
    assert entry.view_scope == "navigation"
