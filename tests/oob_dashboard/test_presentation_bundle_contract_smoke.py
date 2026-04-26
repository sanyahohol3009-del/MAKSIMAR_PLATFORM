from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_contract import (
    PresentationBundleContract,
    PresentationBundleEntry,
    build_presentation_bundle_contract,
)


def test_presentation_bundle_contract_builds() -> None:
    """Presentation bundle contract should build successfully."""
    contract = build_presentation_bundle_contract()

    assert contract.contract_id == "presentation_bundle_contract_001"
    assert contract.total_entries == 4
    assert contract.ready_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_presentation_bundle_contract_contains_expected_entries() -> None:
    """Presentation bundle contract should contain expected canonical entries."""
    contract = build_presentation_bundle_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].presentation_bundle_class
        == "primary_presentation_bundle"
    )
    assert (
        entry_map["display_foundation_secondary"].presentation_bundle_class
        == "secondary_presentation_bundle"
    )
    assert (
        entry_map["display_operator_interaction"].presentation_bundle_class
        == "interaction_presentation_bundle"
    )

    assert entry_map["display_foundation_primary"].dashboard_visible_state_ready is True
    assert entry_map["display_foundation_primary"].display_mapping_consistent is True


def test_presentation_bundle_entry_rejects_non_truth_bound() -> None:
    """Presentation bundle entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical presentation bundles.",
    ):
        PresentationBundleEntry(
            presentation_bundle_id="presentation_bundle_invalid",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_foundation_primary",
            panel_or_surface_id="workspace_operator_main_surface",
            presentation_bundle_state="presentation_bundle_ready",
            presentation_bundle_class="primary_presentation_bundle",
            dashboard_visible_state_ready=True,
            display_mapping_consistent=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid presentation bundle entry.",
        )


def test_presentation_bundle_manual_contract_builds() -> None:
    """Presentation bundle manual contract should build successfully."""
    entries = (
        PresentationBundleEntry(
            presentation_bundle_id="presentation_bundle_001",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_foundation_primary",
            panel_or_surface_id="workspace_operator_main_surface",
            presentation_bundle_state="presentation_bundle_ready",
            presentation_bundle_class="primary_presentation_bundle",
            dashboard_visible_state_ready=True,
            display_mapping_consistent=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical presentation bundle entry.",
        ),
    )

    contract = PresentationBundleContract(
        contract_id="presentation_bundle_contract_001",
        total_entries=1,
        ready_entries=1,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1
    assert contract.ready_entries == 1
