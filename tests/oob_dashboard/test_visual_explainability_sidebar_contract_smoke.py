from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_explainability_sidebar_contract import (
    build_visual_explainability_sidebar_contract,
)


def test_visual_explainability_sidebar_contract_builds() -> None:
    """Visual explainability sidebar contract should build successfully."""
    contract = build_visual_explainability_sidebar_contract()

    assert contract.contract_id == "visual_explainability_sidebar_contract_001"
    assert contract.total_entries > 0
    assert contract.visible_entries == contract.total_entries
    assert contract.read_only_entries == contract.total_entries


def test_visual_explainability_sidebar_contains_system_status_entry() -> None:
    """Explainability sidebar should contain system status entry."""
    contract = build_visual_explainability_sidebar_contract()
    entry = next(
        item for item in contract.entries if item.panel_id == "panel_system_status_001"
    )

    assert entry.sidebar_entry_id == "visual_sidebar_panel_system_status_001"
    assert entry.block_type == "security_block"
    assert entry.sidebar_priority == "primary"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.visible_in_sidebar is True
    assert entry.read_only is True


def test_visual_explainability_sidebar_contains_incidents_entry() -> None:
    """Explainability sidebar should contain incidents entry."""
    contract = build_visual_explainability_sidebar_contract()
    entry = next(
        item for item in contract.entries if item.panel_id == "panel_incidents_001"
    )

    assert entry.block_type in {"diagnostics_block", "explainability_block"}
    assert entry.visible_in_sidebar is True
    assert entry.read_only is True


def test_visual_explainability_sidebar_counts_are_consistent() -> None:
    """Explainability sidebar counts should remain internally consistent."""
    contract = build_visual_explainability_sidebar_contract()

    assert (
        contract.security_block_entries
        + contract.diagnostics_block_entries
        + contract.explainability_block_entries
        == contract.total_entries
    )
    assert (
        contract.primary_entries
        + contract.secondary_entries
        + contract.supporting_entries
        == contract.total_entries
    )
