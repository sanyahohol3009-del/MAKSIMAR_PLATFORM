from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.logical_display_target_contract import (
    LogicalDisplayTargetEntry,
    build_logical_display_target_contract,
)


def test_logical_display_target_contract_builds() -> None:
    """Logical display target contract should build successfully."""
    contract = build_logical_display_target_contract()

    assert contract.contract_id == "logical_display_target_contract_001"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3


def test_logical_display_target_contract_contains_expected_entries() -> None:
    """Logical display target contract should contain expected canonical entries."""
    contract = build_logical_display_target_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].logical_target_class
        == "foundation_primary_logical_target"
    )
    assert (
        entry_map["display_foundation_secondary"].logical_target_class
        == "foundation_secondary_logical_target"
    )
    assert (
        entry_map["display_operator_interaction"].logical_target_class
        == "operator_interaction_logical_target"
    )

    assert (
        entry_map["display_foundation_primary"].fallback_display_target_id
        == "display_foundation_secondary"
    )
    assert (
        entry_map["display_foundation_secondary"].fallback_display_target_id
        == "display_foundation_primary"
    )
    assert (
        entry_map["display_operator_interaction"].fallback_display_target_id
        == "display_operator_interaction"
    )


def test_logical_display_target_entry_rejects_non_operator_visible() -> None:
    """Logical display target entries must remain operator-visible."""
    with pytest.raises(
        ValueError,
        match="operator_visible must remain true for canonical logical display targets.",
    ):
        LogicalDisplayTargetEntry(
            logical_target_id="logical_display_target_invalid",
            display_target_id="display_foundation_primary",
            physical_monitor_id="physical_monitor_001",
            logical_target_state="logical_display_target_ready",
            logical_target_class="foundation_primary_logical_target",
            display_role="foundation_primary_display",
            display_zone="foundation_main_zone",
            fallback_display_target_id="display_foundation_secondary",
            operator_visible=False,
            description="Invalid logical display target entry.",
        )
