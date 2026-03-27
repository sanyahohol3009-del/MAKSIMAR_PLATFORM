from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_display_runtime_resolver_integration_contract,
)


def test_display_runtime_resolver_integration_contract_builds() -> None:
    """Display runtime/resolver integration contract should build successfully."""
    contract = build_display_runtime_resolver_integration_contract()

    assert contract.total_entries == 19
    assert contract.resolved_entries == 18
    assert contract.hidden_internal_entries == 1
    assert contract.runtime_resolved_entries == 18


def test_display_runtime_resolver_chat_entry() -> None:
    """Chat panel should participate in runtime resolution."""
    contract = build_display_runtime_resolver_integration_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.view_id == "view_chat"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.resolver_state == "resolved"
    assert entry.display_availability == "available"
    assert entry.participates_in_runtime_resolution is True


def test_display_runtime_resolver_foundation_runtime_entry() -> None:
    """Foundation runtime panel should resolve to diagnostics display."""
    contract = build_display_runtime_resolver_integration_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.view_id == "view_foundation_runtime"
    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.resolver_state == "resolved"
    assert entry.participates_in_runtime_resolution is True


def test_display_runtime_resolver_navigation_entry() -> None:
    """Navigation panel should remain hidden internal."""
    contract = build_display_runtime_resolver_integration_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.view_id == "view_navigation"
    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.resolver_state == "hidden_internal"
    assert entry.participates_in_runtime_resolution is False
