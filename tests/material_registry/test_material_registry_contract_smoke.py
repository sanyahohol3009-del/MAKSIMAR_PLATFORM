from __future__ import annotations

from MAKSIMAR_CORE_LIB.material_registry import (
    build_material_registry_contract,
)


def test_material_registry_contract_builds() -> None:
    """Material registry contract should build successfully."""
    contract = build_material_registry_contract()

    assert contract.total_entries == 4
    assert contract.production_usable_entries == 4
    assert contract.brittle_entries == 1
    assert contract.high_reflectivity_entries == 1
    assert contract.registered_entries == 4


def test_material_registry_contract_contains_expected_aluminum_entry() -> None:
    """Material registry should expose expected aluminum entry."""
    contract = build_material_registry_contract()
    entry = contract.entries[0]

    assert entry.material_id == "material_aluminum_001"
    assert entry.display_name == "Aluminum"
    assert entry.density_kg_m3 == 2700
    assert entry.thermal_behavior == "high_conductivity"
    assert entry.fracture_profile == "ductile"


def test_material_registry_contract_contains_expected_steel_entry() -> None:
    """Material registry should expose expected steel entry."""
    contract = build_material_registry_contract()
    entry = contract.entries[1]

    assert entry.material_id == "material_steel_001"
    assert entry.display_name == "Steel"
    assert entry.density_kg_m3 == 7850
    assert entry.thermal_behavior == "medium_conductivity"
    assert entry.fracture_profile == "ductile"


def test_material_registry_contract_contains_expected_acrylic_entry() -> None:
    """Material registry should expose expected acrylic entry."""
    contract = build_material_registry_contract()
    entry = contract.entries[2]

    assert entry.material_id == "material_acrylic_001"
    assert entry.display_name == "Acrylic"
    assert entry.density_kg_m3 == 1180
    assert entry.thermal_behavior == "low_conductivity"
    assert entry.fracture_profile == "brittle"


def test_material_registry_contract_contains_expected_wood_entry() -> None:
    """Material registry should expose expected wood entry."""
    contract = build_material_registry_contract()
    entry = contract.entries[3]

    assert entry.material_id == "material_wood_001"
    assert entry.display_name == "Wood"
    assert entry.density_kg_m3 == 700
    assert entry.thermal_behavior == "low_conductivity"
    assert entry.fracture_profile == "anisotropic"
