from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_placement_routing_contract import (
    DisplayPlacementRoutingEntry,
    build_display_placement_routing_contract,
)


def test_display_placement_routing_contract_builds() -> None:
    """Display placement routing contract should build successfully."""
    contract = build_display_placement_routing_contract()

    assert contract.contract_id == "display_placement_routing_contract_001"
    assert contract.total_entries == 2
    assert contract.pinned_route_entries == 1
    assert contract.replaceable_route_entries == 1
    assert contract.operator_visible_entries == 2


def test_display_placement_routing_contract_contains_expected_entries() -> None:
    """Display placement routing contract should contain expected canonical entries."""
    contract = build_display_placement_routing_contract()
    entry_map = {entry.routing_id: entry for entry in contract.entries}

    pinned_entry = entry_map["display_placement_route_001"]
    replaceable_entry = entry_map["display_placement_route_002"]

    assert pinned_entry.display_target_id == "display_foundation_primary"
    assert pinned_entry.routing_class == "pinned_route"
    assert pinned_entry.candidate_display_target_id is None

    assert replaceable_entry.display_target_id == "display_foundation_secondary"
    assert replaceable_entry.routing_class == "replaceable_route"
    assert replaceable_entry.candidate_display_target_id == "display_foundation_secondary"


def test_display_placement_routing_entry_rejects_missing_candidate() -> None:
    """Replaceable routes must expose candidate display ids."""
    with pytest.raises(
        ValueError,
        match="replaceable_route entries must expose candidate_display_target_id.",
    ):
        DisplayPlacementRoutingEntry(
            routing_id="display_placement_route_invalid",
            display_target_id="display_foundation_secondary",
            routing_state="placement_route_resolved",
            routing_class="replaceable_route",
            incumbent_assignment_id="display_assignment_002",
            candidate_display_target_id=None,
            operator_visible=True,
            description="Invalid placement routing entry.",
        )
