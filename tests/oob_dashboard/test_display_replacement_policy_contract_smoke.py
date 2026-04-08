from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_replacement_policy_contract import (
    DisplayReplacementPolicyEntry,
    build_display_replacement_policy_contract,
)


def test_display_replacement_policy_contract_builds() -> None:
    """Display replacement-policy contract should build successfully."""
    contract = build_display_replacement_policy_contract()

    assert contract.contract_id == "display_replacement_policy_contract_001"
    assert contract.total_entries == 3
    assert contract.not_replaceable_entries == 1
    assert contract.replaceable_entries == 2
    assert contract.operator_visible_entries == 3


def test_display_replacement_policy_contract_contains_expected_entries() -> None:
    """Display replacement-policy contract should contain expected canonical entries."""
    contract = build_display_replacement_policy_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_primary_operator"].replacement_decision == "not_replaceable"
    assert entry_map["display_primary_operator"].replacement_class == "pinned_primary_surface"

    assert entry_map["display_secondary_diagnostics"].replacement_decision == "replaceable_without_disruption"
    assert entry_map["display_secondary_diagnostics"].replacement_class == "replaceable_secondary_surface"

    assert entry_map["display_tertiary_expansion"].replacement_decision == "replaceable_without_disruption"
    assert entry_map["display_tertiary_expansion"].replacement_class == "replaceable_tertiary_surface"


def test_display_replacement_policy_entry_rejects_bad_totals() -> None:
    """Display replacement-policy entry should reject inconsistent totals."""
    with pytest.raises(ValueError, match="active_assignments must equal"):
        DisplayReplacementPolicyEntry(
            display_target_id="display_primary_operator",
            replacement_decision="not_replaceable",
            replacement_class="pinned_primary_surface",
            active_assignments=2,
            replaceable_assignments=0,
            pinned_assignments=1,
            operator_visible=True,
            description="Invalid replacement policy totals.",
        )
