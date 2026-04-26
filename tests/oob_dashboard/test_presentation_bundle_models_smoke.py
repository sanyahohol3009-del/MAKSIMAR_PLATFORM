from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_models import (
    PresentationBundleRuntimeContract,
    PresentationBundleRuntimeEntry,
)


def test_presentation_bundle_runtime_entry_builds() -> None:
    """Presentation-bundle runtime entry should build successfully."""
    entry = PresentationBundleRuntimeEntry(
        presentation_bundle_runtime_id="presentation_bundle_runtime_001",
        display_target_id="display_foundation_primary",
        workspace_id="workspace_foundation_monitoring",
        presentation_bundle_runtime_state="presentation_bundle_runtime_ready",
        presentation_bundle_runtime_class="foundation_presentation_runtime",
        presentation_bundle_runtime_mode="assembled_foundation_presentation_runtime",
        visible_state_ready=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical presentation-bundle runtime entry.",
    )

    assert entry.presentation_bundle_runtime_id == "presentation_bundle_runtime_001"
    assert entry.presentation_bundle_runtime_state == "presentation_bundle_runtime_ready"
    assert entry.presentation_bundle_runtime_class == "foundation_presentation_runtime"


def test_presentation_bundle_runtime_entry_rejects_non_truth_bound() -> None:
    """Presentation-bundle runtime entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical presentation-bundle runtime entries.",
    ):
        PresentationBundleRuntimeEntry(
            presentation_bundle_runtime_id="presentation_bundle_runtime_invalid",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            presentation_bundle_runtime_state="presentation_bundle_runtime_ready",
            presentation_bundle_runtime_class="foundation_presentation_runtime",
            presentation_bundle_runtime_mode="assembled_foundation_presentation_runtime",
            visible_state_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid presentation-bundle runtime entry.",
        )


def test_presentation_bundle_runtime_contract_builds() -> None:
    """Presentation-bundle runtime contract should build successfully."""
    entries = (
        PresentationBundleRuntimeEntry(
            presentation_bundle_runtime_id="presentation_bundle_runtime_001",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            presentation_bundle_runtime_state="presentation_bundle_runtime_ready",
            presentation_bundle_runtime_class="foundation_presentation_runtime",
            presentation_bundle_runtime_mode="assembled_foundation_presentation_runtime",
            visible_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Foundation runtime entry.",
        ),
        PresentationBundleRuntimeEntry(
            presentation_bundle_runtime_id="presentation_bundle_runtime_002",
            display_target_id="display_operator_interaction",
            workspace_id="workspace_operator_interaction",
            presentation_bundle_runtime_state="presentation_bundle_runtime_ready",
            presentation_bundle_runtime_class="interaction_presentation_runtime",
            presentation_bundle_runtime_mode="assembled_interaction_presentation_runtime",
            visible_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Interaction runtime entry.",
        ),
    )

    contract = PresentationBundleRuntimeContract(
        contract_id="presentation_bundle_runtime_contract_001",
        total_entries=2,
        foundation_runtime_entries=1,
        interaction_runtime_entries=1,
        operator_visible_entries=2,
        truth_bound_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.foundation_runtime_entries == 1
    assert contract.interaction_runtime_entries == 1
