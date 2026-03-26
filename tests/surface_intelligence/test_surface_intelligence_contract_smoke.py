from __future__ import annotations

from MAKSIMAR_CORE_LIB.surface_intelligence import (
    build_surface_intelligence_contract,
)


def test_surface_intelligence_contract_builds() -> None:
    """Surface intelligence contract should build successfully."""
    contract = build_surface_intelligence_contract()

    assert contract.total_entries == 4
    assert contract.fine_resolution_entries == 2
    assert contract.production_usable_entries == 4
    assert contract.explainable_entries == 4
    assert contract.defined_entries == 4


def test_surface_intelligence_contract_contains_expected_aluminum_entry() -> None:
    """Surface intelligence should expose expected aluminum entry."""
    contract = build_surface_intelligence_contract()
    entry = contract.entries[0]

    assert entry.surface_entry_id == "surfaceintel_aluminum_engraving_001"
    assert entry.scan_mode == "full_surface_scan"
    assert entry.height_map_resolution_class == "fine"
    assert entry.tool_profile_class == "engraving_tip"
    assert entry.material_id == "material_aluminum_001"


def test_surface_intelligence_contract_contains_expected_steel_entry() -> None:
    """Surface intelligence should expose expected steel entry."""
    contract = build_surface_intelligence_contract()
    entry = contract.entries[1]

    assert entry.surface_entry_id == "surfaceintel_steel_cutting_001"
    assert entry.scan_mode == "full_surface_scan"
    assert entry.height_map_resolution_class == "fine"
    assert entry.tool_profile_class == "cutting_head"
    assert entry.material_id == "material_steel_001"


def test_surface_intelligence_contract_contains_expected_acrylic_entry() -> None:
    """Surface intelligence should expose expected acrylic entry."""
    contract = build_surface_intelligence_contract()
    entry = contract.entries[2]

    assert entry.surface_entry_id == "surfaceintel_acrylic_engraving_001"
    assert entry.scan_mode == "full_surface_scan"
    assert entry.height_map_resolution_class == "medium"
    assert entry.tool_profile_class == "engraving_tip"
    assert entry.material_id == "material_acrylic_001"


def test_surface_intelligence_contract_contains_expected_wood_entry() -> None:
    """Surface intelligence should expose expected wood entry."""
    contract = build_surface_intelligence_contract()
    entry = contract.entries[3]

    assert entry.surface_entry_id == "surfaceintel_wood_engraving_001"
    assert entry.scan_mode == "full_surface_scan"
    assert entry.height_map_resolution_class == "medium"
    assert entry.tool_profile_class == "engraving_tip"
    assert entry.material_id == "material_wood_001"
