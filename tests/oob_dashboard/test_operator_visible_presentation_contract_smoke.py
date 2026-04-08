from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_visible_presentation_contract import (
    OperatorVisiblePresentationEntry,
    build_operator_visible_presentation_contract,
)


def test_operator_visible_presentation_contract_builds() -> None:
    """Operator-visible presentation contract should build successfully."""
    contract = build_operator_visible_presentation_contract()

    assert contract.contract_id == "operator_visible_presentation_contract_001"
    assert contract.total_entries == 3
    assert contract.shared_surface_entries == 1
    assert contract.projection_ready_entries == 3
    assert contract.operator_visible_entries == 3


def test_operator_visible_presentation_contract_contains_expected_entries() -> None:
    """Operator-visible presentation contract should contain expected canonical entries."""
    contract = build_operator_visible_presentation_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_primary_operator"].presentation_class == "primary_operator_presentation"
    assert entry_map["display_primary_operator"].interaction_surface_id == "main_operator_interaction_surface_001"

    assert entry_map["display_secondary_diagnostics"].presentation_class == "secondary_operator_presentation"
    assert entry_map["display_secondary_diagnostics"].shared_surface is True

    assert entry_map["display_tertiary_expansion"].presentation_class == "tertiary_operator_presentation"
    assert entry_map["display_tertiary_expansion"].projection_ready is True


def test_operator_visible_presentation_entry_rejects_not_ready_projection() -> None:
    """Operator-visible presentation entries must remain projection-ready."""
    with pytest.raises(ValueError, match="projection_ready must remain true"):
        OperatorVisiblePresentationEntry(
            presentation_id="operator_visible_presentation_invalid",
            display_target_id="display_primary_operator",
            interaction_surface_id="main_operator_interaction_surface_001",
            presentation_state="presentation_ready",
            presentation_class="primary_operator_presentation",
            projection_ready=False,
            shared_surface=False,
            operator_visible=True,
            description="Invalid operator-visible presentation entry.",
        )
