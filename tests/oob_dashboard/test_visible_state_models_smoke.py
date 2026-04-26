from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visible_state_models import (
    VisibleStateContract,
    VisibleStateEntry,
)


def test_visible_state_entry_builds() -> None:
    """Visible state entry should build successfully."""
    entry = VisibleStateEntry(
        visible_state_id="visible_state_001",
        display_target_id="display_foundation_primary",
        workspace_id="workspace_foundation_monitoring",
        visible_state_state="visible_state_ready",
        visible_state_class="foundation_visible_state",
        visible_state_mode="assembled_foundation_visible_state",
        final_visible_screen_state_ready=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visible state entry.",
    )

    assert entry.visible_state_id == "visible_state_001"
    assert entry.visible_state_state == "visible_state_ready"
    assert entry.visible_state_class == "foundation_visible_state"


def test_visible_state_entry_rejects_non_truth_bound() -> None:
    """Visible state entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical visible state entries.",
    ):
        VisibleStateEntry(
            visible_state_id="visible_state_invalid",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            visible_state_state="visible_state_ready",
            visible_state_class="foundation_visible_state",
            visible_state_mode="assembled_foundation_visible_state",
            final_visible_screen_state_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid visible state entry.",
        )


def test_visible_state_contract_builds() -> None:
    """Visible state contract should build successfully."""
    entries = (
        VisibleStateEntry(
            visible_state_id="visible_state_001",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            visible_state_state="visible_state_ready",
            visible_state_class="foundation_visible_state",
            visible_state_mode="assembled_foundation_visible_state",
            final_visible_screen_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Foundation visible state entry.",
        ),
        VisibleStateEntry(
            visible_state_id="visible_state_002",
            display_target_id="display_operator_interaction",
            workspace_id="workspace_operator_interaction",
            visible_state_state="visible_state_ready",
            visible_state_class="interaction_visible_state",
            visible_state_mode="assembled_interaction_visible_state",
            final_visible_screen_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Interaction visible state entry.",
        ),
    )

    contract = VisibleStateContract(
        contract_id="visible_state_contract_001",
        total_entries=2,
        foundation_visible_entries=1,
        interaction_visible_entries=1,
        operator_visible_entries=2,
        truth_bound_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.foundation_visible_entries == 1
    assert contract.interaction_visible_entries == 1
