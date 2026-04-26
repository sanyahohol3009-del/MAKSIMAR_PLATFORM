from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.final_screen_state_models import (
    FinalScreenStateContract,
    FinalScreenStateEntry,
)


def test_final_screen_state_entry_builds() -> None:
    """Final screen state entry should build successfully."""
    entry = FinalScreenStateEntry(
        final_screen_state_id="final_screen_state_001",
        display_target_id="display_foundation_primary",
        workspace_id="workspace_foundation_monitoring",
        final_screen_state_state="final_screen_state_ready",
        final_screen_state_class="foundation_final_screen_state",
        final_screen_state_mode="assembled_foundation_final_screen_state",
        final_visible_screen_state_ready=True,
        presentation_bundle_runtime_ready=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical final screen state entry.",
    )

    assert entry.final_screen_state_id == "final_screen_state_001"
    assert entry.final_screen_state_state == "final_screen_state_ready"
    assert entry.final_screen_state_class == "foundation_final_screen_state"


def test_final_screen_state_entry_rejects_non_truth_bound() -> None:
    """Final screen state entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical final screen state entries.",
    ):
        FinalScreenStateEntry(
            final_screen_state_id="final_screen_state_invalid",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            final_screen_state_state="final_screen_state_ready",
            final_screen_state_class="foundation_final_screen_state",
            final_screen_state_mode="assembled_foundation_final_screen_state",
            final_visible_screen_state_ready=True,
            presentation_bundle_runtime_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid final screen state entry.",
        )


def test_final_screen_state_contract_builds() -> None:
    """Final screen state contract should build successfully."""
    entries = (
        FinalScreenStateEntry(
            final_screen_state_id="final_screen_state_001",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            final_screen_state_state="final_screen_state_ready",
            final_screen_state_class="foundation_final_screen_state",
            final_screen_state_mode="assembled_foundation_final_screen_state",
            final_visible_screen_state_ready=True,
            presentation_bundle_runtime_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Foundation final screen state entry.",
        ),
        FinalScreenStateEntry(
            final_screen_state_id="final_screen_state_002",
            display_target_id="display_operator_interaction",
            workspace_id="workspace_operator_interaction",
            final_screen_state_state="final_screen_state_ready",
            final_screen_state_class="interaction_final_screen_state",
            final_screen_state_mode="assembled_interaction_final_screen_state",
            final_visible_screen_state_ready=True,
            presentation_bundle_runtime_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Interaction final screen state entry.",
        ),
    )

    contract = FinalScreenStateContract(
        contract_id="final_screen_state_contract_001",
        total_entries=2,
        foundation_final_entries=1,
        interaction_final_entries=1,
        operator_visible_entries=2,
        truth_bound_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.foundation_final_entries == 1
    assert contract.interaction_final_entries == 1
