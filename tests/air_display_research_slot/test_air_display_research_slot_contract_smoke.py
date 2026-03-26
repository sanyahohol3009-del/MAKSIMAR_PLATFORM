from __future__ import annotations

from MAKSIMAR_CORE_LIB.air_display_research_slot import (
    build_air_display_research_slot_contract,
)


def test_air_display_research_slot_contract_builds() -> None:
    """Air display research slot contract should build successfully."""
    contract = build_air_display_research_slot_contract()

    assert contract.total_entries == 3
    assert contract.research_only_entries == 3
    assert contract.production_forbidden_entries == 3
    assert contract.explainable_entries == 3
    assert contract.defined_entries == 3


def test_air_display_research_slot_contract_contains_expected_projection_entry() -> None:
    """Air display research slot should expose expected projection entry."""
    contract = build_air_display_research_slot_contract()
    entry = contract.entries[0]

    assert entry.research_entry_id == "airdisplay_projection_assisted_001"
    assert entry.research_mode == "projection_assisted_research"
    assert entry.linked_optics_engine_id == "opticsengine_projection_assisted_spatial_001"
    assert entry.linked_integration_entry_id == "wristdisplayint_engineering_001"
    assert entry.production_path_allowed is False


def test_air_display_research_slot_contract_contains_expected_scattering_entry() -> None:
    """Air display research slot should expose expected scattering entry."""
    contract = build_air_display_research_slot_contract()
    entry = contract.entries[1]

    assert entry.research_entry_id == "airdisplay_controlled_scattering_001"
    assert entry.research_mode == "controlled_scattering_research"
    assert entry.linked_optics_engine_id == "opticsengine_controlled_scattering_research_001"
    assert entry.linked_integration_entry_id == "wristdisplayint_ar_001"
    assert entry.production_path_allowed is False


def test_air_display_research_slot_contract_contains_expected_intersection_entry() -> None:
    """Air display research slot should expose expected intersection entry."""
    contract = build_air_display_research_slot_contract()
    entry = contract.entries[2]

    assert entry.research_entry_id == "airdisplay_beam_intersection_001"
    assert entry.research_mode == "beam_intersection_research"
    assert entry.linked_optics_engine_id == "opticsengine_beam_intersection_research_001"
    assert entry.linked_integration_entry_id == "wristdisplayint_ar_001"
    assert entry.production_path_allowed is False
