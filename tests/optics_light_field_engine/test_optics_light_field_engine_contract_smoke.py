from __future__ import annotations

from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)


def test_optics_light_field_engine_contract_builds() -> None:
    """Optics light field engine contract should build successfully."""
    contract = build_optics_light_field_engine_contract()

    assert contract.total_entries == 4
    assert contract.private_display_entries == 1
    assert contract.shared_projection_entries == 1
    assert contract.research_only_entries == 2
    assert contract.execution_allowed_entries == 1
    assert contract.defined_entries == 4


def test_optics_light_field_engine_contract_contains_expected_ar_entry() -> None:
    """Optics engine should expose expected AR entry."""
    contract = build_optics_light_field_engine_contract()
    entry = contract.entries[0]

    assert entry.engine_entry_id == "opticsengine_ar_glasses_projection_001"
    assert entry.optics_mode == "ar_glasses_projection"
    assert entry.simulation_mode == "strict_physics"
    assert entry.beam_model_class == "guided_projection"
    assert entry.display_mode_selection == "ar_glasses_display"
    assert entry.execution_eligibility == "allowed_for_private_display"


def test_optics_light_field_engine_contract_contains_expected_projection_entry() -> None:
    """Optics engine should expose expected projection entry."""
    contract = build_optics_light_field_engine_contract()
    entry = contract.entries[1]

    assert entry.engine_entry_id == "opticsengine_projection_assisted_spatial_001"
    assert entry.optics_mode == "projection_assisted_spatial"
    assert entry.simulation_mode == "engineering_realistic"
    assert entry.beam_model_class == "free_space_projection"
    assert entry.display_mode_selection == "wall_projection_display"
    assert entry.execution_eligibility == "requires_validation_gate"


def test_optics_light_field_engine_contract_contains_expected_scattering_entry() -> None:
    """Optics engine should expose expected controlled scattering research entry."""
    contract = build_optics_light_field_engine_contract()
    entry = contract.entries[2]

    assert entry.engine_entry_id == "opticsengine_controlled_scattering_research_001"
    assert entry.optics_mode == "controlled_scattering_research"
    assert entry.simulation_mode == "research_relaxed"
    assert entry.beam_model_class == "controlled_scattering"
    assert entry.display_mode_selection == "research_optics_display"
    assert entry.execution_eligibility == "forbidden_for_execution"


def test_optics_light_field_engine_contract_contains_expected_intersection_entry() -> None:
    """Optics engine should expose expected beam intersection research entry."""
    contract = build_optics_light_field_engine_contract()
    entry = contract.entries[3]

    assert entry.engine_entry_id == "opticsengine_beam_intersection_research_001"
    assert entry.optics_mode == "beam_intersection_research"
    assert entry.simulation_mode == "control_learning"
    assert entry.beam_model_class == "intersection_field"
    assert entry.display_mode_selection == "research_optics_display"
    assert entry.execution_eligibility == "forbidden_for_execution"
