from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_display_target_vocabulary_contract,
)


def test_display_target_vocabulary_contract_builds() -> None:
    """Display target vocabulary contract should build successfully."""
    contract = build_display_target_vocabulary_contract()

    assert contract.total_entries == 3
    assert contract.physical_monitor_entries == 2
    assert contract.logical_surface_entries == 1


def test_display_target_vocabulary_primary_operator_entry() -> None:
    """Primary operator display should expose canonical semantics."""
    contract = build_display_target_vocabulary_contract()
    entry = contract.entries[0]

    assert entry.display_target_id == "display_primary_operator"
    assert entry.display_role == "primary_operator"
    assert entry.display_zone == "center"
    assert entry.display_target_type == "physical_monitor"
    assert entry.display_title == "Primary Operator Display"


def test_display_target_vocabulary_diagnostics_entry() -> None:
    """Diagnostics display should expose canonical semantics."""
    contract = build_display_target_vocabulary_contract()
    entry = contract.entries[1]

    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.display_role == "diagnostics"
    assert entry.display_zone == "right"
    assert entry.display_target_type == "physical_monitor"


def test_display_target_vocabulary_expansion_entry() -> None:
    """Expansion display should expose canonical semantics."""
    contract = build_display_target_vocabulary_contract()
    entry = contract.entries[2]

    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.display_role == "expansion"
    assert entry.display_zone == "left"
    assert entry.display_target_type == "logical_surface"
