from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_binding_contract,
)


def test_panel_binding_contract_builds() -> None:
    """Panel binding contract should build successfully."""
    contract = build_panel_binding_contract()

    assert contract.total_entries == 19
    assert contract.primary_operator_bindings == 3
    assert contract.diagnostics_bindings == 8
    assert contract.expansion_bindings == 8
    assert contract.default_target_bindings == 19


def test_panel_binding_chat_entry() -> None:
    """Chat panel should bind to primary operator display."""
    contract = build_panel_binding_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.display_target_id == "display_primary_operator"
    assert entry.binding_reason == "operator_surface_binding"
    assert entry.is_default_target is True
    assert entry.eligible_for_main_dashboard is True
    assert entry.eligible_for_oob_dashboard is False


def test_panel_binding_foundation_runtime_entry() -> None:
    """Foundation runtime panel should bind to diagnostics display."""
    contract = build_panel_binding_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.binding_reason == "foundation_monitoring_binding"
    assert entry.eligible_for_main_dashboard is True
    assert entry.eligible_for_oob_dashboard is True


def test_panel_binding_navigation_entry() -> None:
    """Navigation panel should bind to expansion display as hidden internal."""
    contract = build_panel_binding_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.binding_reason == "hidden_internal_binding"
    assert entry.eligible_for_main_dashboard is False
    assert entry.eligible_for_oob_dashboard is False
