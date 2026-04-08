from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_presentation_bundle_contract import (
    OperatorPresentationBundleEntry,
    build_operator_presentation_bundle_contract,
)


def test_operator_presentation_bundle_contract_builds() -> None:
    """Operator presentation bundle contract should build successfully."""
    contract = build_operator_presentation_bundle_contract()

    assert contract.contract_id == "operator_presentation_bundle_contract_001"
    assert contract.total_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.ready_entries == 1


def test_operator_presentation_bundle_contract_contains_expected_entry() -> None:
    """Operator presentation bundle contract should contain expected canonical entry."""
    contract = build_operator_presentation_bundle_contract()
    entry = contract.entries[0]

    assert entry.bundle_id == "operator_presentation_bundle_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.interaction_surface_id == "main_operator_interaction_surface_001"
    assert entry.bundle_state == "operator_bundle_ready"
    assert entry.bundle_class == "primary_operator_bundle"
    assert entry.presentation_entries == 3
    assert entry.action_queue_panel_present is True
    assert entry.approval_queue_panel_present is True
    assert entry.audit_timeline_panel_present is True
    assert entry.operator_visible is True


def test_operator_presentation_bundle_entry_rejects_missing_action_queue() -> None:
    """Operator presentation bundle entries must include action queue presence."""
    with pytest.raises(ValueError, match="action_queue_panel_present must remain true"):
        OperatorPresentationBundleEntry(
            bundle_id="operator_presentation_bundle_invalid",
            workspace_id="workspace_operator_main",
            interaction_surface_id="main_operator_interaction_surface_001",
            bundle_state="operator_bundle_ready",
            bundle_class="primary_operator_bundle",
            presentation_entries=3,
            action_queue_panel_present=False,
            approval_queue_panel_present=True,
            audit_timeline_panel_present=True,
            operator_visible=True,
            description="Invalid operator presentation bundle entry.",
        )
