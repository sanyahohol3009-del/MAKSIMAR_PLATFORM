from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    DisplayAssignmentRegistryEntry,
    build_display_assignment_registry_contract,
)


def test_display_assignment_registry_contract_builds() -> None:
    """Display assignment registry contract should build successfully."""
    contract = build_display_assignment_registry_contract()

    assert contract.contract_id == "display_assignment_registry_contract_001"
    assert contract.total_entries == 4
    assert contract.active_entries == 4
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 4


def test_display_assignment_registry_contract_contains_expected_entries() -> None:
    """Display assignment registry contract should contain expected canonical entries."""
    contract = build_display_assignment_registry_contract()
    entry_map = {entry.assignment_id: entry for entry in contract.entries}

    assert (
        entry_map["display_assignment_001"].display_target_id
        == "display_foundation_primary"
    )
    assert entry_map["display_assignment_001"].replaceable is False
    assert (
        entry_map["display_assignment_001"].assignment_role
        == "foundation_primary_surface"
    )

    assert (
        entry_map["display_assignment_002"].display_target_id
        == "display_foundation_secondary"
    )
    assert entry_map["display_assignment_002"].replaceable is True

    assert (
        entry_map["display_assignment_003"].display_target_id
        == "display_foundation_secondary"
    )
    assert entry_map["display_assignment_003"].replaceable is True

    assert (
        entry_map["display_assignment_004"].display_target_id
        == "display_operator_interaction"
    )
    assert (
        entry_map["display_assignment_004"].assignment_role
        == "operator_interaction_surface"
    )


def test_display_assignment_registry_entry_rejects_blank_id() -> None:
    """Display assignment registry entry should reject blank ids."""
    with pytest.raises(ValueError, match="assignment_id must be a non-empty string."):
        DisplayAssignmentRegistryEntry(
            assignment_id="",
            display_target_id="display_foundation_primary",
            panel_or_surface_id="workspace_foundation_monitoring_surface",
            assignment_role="foundation_primary_surface",
            assignment_state="display_assignment_active",
            workspace_id="workspace_foundation_monitoring",
            replaceable=False,
            operator_visible=True,
            description="Invalid display assignment entry.",
        )
