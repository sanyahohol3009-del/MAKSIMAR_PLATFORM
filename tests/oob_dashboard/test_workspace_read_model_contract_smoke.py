from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_workspace_read_model_contract,
)


def test_workspace_read_model_contract_builds() -> None:
    """Workspace read model contract should build successfully."""
    contract = build_workspace_read_model_contract()

    assert contract.total_entries == 3
    assert contract.read_only_entries == 2
    assert contract.operator_surface_entries == 1


def test_workspace_read_model_foundation_entry() -> None:
    """Foundation monitoring workspace read model should be canonical."""
    contract = build_workspace_read_model_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.workspace_id == "workspace_foundation_monitoring"
    )

    assert entry.workspace_role == "foundation_monitoring"
    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.total_panels == 8
    assert entry.main_focus_panels == 4
    assert entry.diagnostics_panels == 2
    assert entry.sidebar_panels == 2
    assert entry.secondary_panels == 0
    assert entry.read_only is True


def test_workspace_read_model_operator_entry() -> None:
    """Operator main workspace read model should be canonical."""
    contract = build_workspace_read_model_contract()
    entry = next(
        entry for entry in contract.entries if entry.workspace_id == "workspace_operator_main"
    )

    assert entry.workspace_role == "operator_surface"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.total_panels == 3
    assert entry.main_focus_panels == 2
    assert entry.diagnostics_panels == 0
    assert entry.sidebar_panels == 0
    assert entry.secondary_panels == 1
    assert entry.read_only is False


def test_workspace_read_model_expansion_entry() -> None:
    """Expansion observability workspace read model should be canonical."""
    contract = build_workspace_read_model_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.workspace_id == "workspace_expansion_observability"
    )

    assert entry.workspace_role == "expansion_surface"
    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.total_panels == 8
    assert entry.main_focus_panels == 0
    assert entry.diagnostics_panels == 0
    assert entry.sidebar_panels == 0
    assert entry.secondary_panels == 8
    assert entry.read_only is True
