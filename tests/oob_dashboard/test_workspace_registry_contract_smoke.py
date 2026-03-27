from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_workspace_registry_contract,
)


def test_workspace_registry_contract_builds() -> None:
    """Workspace registry contract should build successfully."""
    contract = build_workspace_registry_contract()

    assert contract.total_entries == 3
    assert contract.read_only_entries == 2
    assert contract.operator_surface_entries == 1


def test_workspace_registry_foundation_monitoring_entry() -> None:
    """Foundation monitoring workspace should be canonical and read-only."""
    contract = build_workspace_registry_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.workspace_id == "workspace_foundation_monitoring"
    )

    assert entry.workspace_role == "foundation_monitoring"
    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.default_panel_count == 8
    assert entry.read_only is True


def test_workspace_registry_operator_main_entry() -> None:
    """Operator main workspace should be canonical operator surface."""
    contract = build_workspace_registry_contract()
    entry = next(
        entry for entry in contract.entries if entry.workspace_id == "workspace_operator_main"
    )

    assert entry.workspace_role == "operator_surface"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.default_panel_count == 3
    assert entry.read_only is False


def test_workspace_registry_expansion_entry() -> None:
    """Expansion workspace should be canonical observability surface."""
    contract = build_workspace_registry_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.workspace_id == "workspace_expansion_observability"
    )

    assert entry.workspace_role == "expansion_surface"
    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.default_panel_count == 8
    assert entry.read_only is True
