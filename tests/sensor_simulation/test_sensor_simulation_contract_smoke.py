from __future__ import annotations

from MAKSIMAR_CORE_LIB.sensor_simulation import (
    build_sensor_simulation_contract,
)


def test_sensor_simulation_contract_builds() -> None:
    """Sensor simulation contract should build successfully."""
    contract = build_sensor_simulation_contract()

    assert contract.total_entries == 4
    assert contract.high_fidelity_entries == 1
    assert contract.validation_gate_entries == 2
    assert contract.production_usable_entries == 4
    assert contract.defined_entries == 4


def test_sensor_simulation_contract_contains_expected_aluminum_entry() -> None:
    """Sensor simulation should expose expected aluminum entry."""
    contract = build_sensor_simulation_contract()
    entry = contract.entries[0]

    assert entry.sensor_entry_id == "sensorsim_aluminum_001"
    assert entry.surface_entry_id == "surfaceintel_aluminum_engraving_001"
    assert entry.material_id == "material_aluminum_001"
    assert entry.noise_model_class == "low_noise"
    assert entry.reflection_model_class == "reflective_adjusted"
    assert entry.output_quality == "high_fidelity"


def test_sensor_simulation_contract_contains_expected_steel_entry() -> None:
    """Sensor simulation should expose expected steel entry."""
    contract = build_sensor_simulation_contract()
    entry = contract.entries[1]

    assert entry.sensor_entry_id == "sensorsim_steel_001"
    assert entry.surface_entry_id == "surfaceintel_steel_cutting_001"
    assert entry.material_id == "material_steel_001"
    assert entry.noise_model_class == "medium_noise"
    assert entry.reflection_model_class == "reflective_adjusted"
    assert entry.output_quality == "engineering_grade"


def test_sensor_simulation_contract_contains_expected_acrylic_entry() -> None:
    """Sensor simulation should expose expected acrylic entry."""
    contract = build_sensor_simulation_contract()
    entry = contract.entries[2]

    assert entry.sensor_entry_id == "sensorsim_acrylic_001"
    assert entry.surface_entry_id == "surfaceintel_acrylic_engraving_001"
    assert entry.material_id == "material_acrylic_001"
    assert entry.noise_model_class == "medium_noise"
    assert entry.reflection_model_class == "diffuse_weighted"
    assert entry.output_quality == "engineering_grade"


def test_sensor_simulation_contract_contains_expected_wood_entry() -> None:
    """Sensor simulation should expose expected wood entry."""
    contract = build_sensor_simulation_contract()
    entry = contract.entries[3]

    assert entry.sensor_entry_id == "sensorsim_wood_001"
    assert entry.surface_entry_id == "surfaceintel_wood_engraving_001"
    assert entry.material_id == "material_wood_001"
    assert entry.noise_model_class == "medium_noise"
    assert entry.reflection_model_class == "diffuse_weighted"
    assert entry.output_quality == "engineering_grade"
