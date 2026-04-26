from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_visual_projection_contract import (
    DisplayVisualProjectionEntry,
    build_display_visual_projection_contract,
)


def test_display_visual_projection_contract_builds() -> None:
    """Display visual projection contract should build successfully."""
    contract = build_display_visual_projection_contract()

    assert contract.contract_id == "display_visual_projection_contract_001"
    assert contract.total_entries == 3
    assert contract.shared_surface_entries == 1
    assert contract.ready_entries == 3
    assert contract.operator_visible_entries == 3


def test_display_visual_projection_contract_contains_expected_entries() -> None:
    """Display visual projection contract should contain expected canonical entries."""
    contract = build_display_visual_projection_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].projection_class
        == "foundation_primary_projection"
    )
    assert entry_map["display_foundation_primary"].shared_surface is False

    assert (
        entry_map["display_foundation_secondary"].projection_class
        == "foundation_secondary_projection"
    )
    assert entry_map["display_foundation_secondary"].shared_surface is True

    assert (
        entry_map["display_operator_interaction"].projection_class
        == "operator_interaction_projection"
    )
    assert entry_map["display_operator_interaction"].shared_surface is False


def test_display_visual_projection_entry_rejects_not_ready_projection() -> None:
    """Display visual projection entries must remain projection-ready."""
    with pytest.raises(ValueError, match="projection_ready must remain true"):
        DisplayVisualProjectionEntry(
            projection_id="display_visual_projection_invalid",
            display_target_id="display_foundation_primary",
            projection_state="projection_ready",
            projection_class="foundation_primary_projection",
            selected_assignment_present=True,
            shared_surface=False,
            projection_ready=False,
            operator_visible=True,
            description="Invalid visual projection entry.",
        )
