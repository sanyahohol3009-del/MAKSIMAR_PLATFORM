from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.validation_assets_panel_contract import (
    build_validation_assets_panel_contract,
)


def test_validation_assets_panel_contract_builds() -> None:
    contract = build_validation_assets_panel_contract()

    assert contract.panel_id == "panel_validation_assets"
    assert contract.total_entries == 3
    assert contract.validated_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_validation_assets_panel_contract_contains_expected_entries() -> None:
    contract = build_validation_assets_panel_contract()

    states = tuple(
        (entry.asset_id, entry.validation_state, entry.asset_kind)
        for entry in contract.entries
    )

    assert states == (
        ("validation_asset_surface_map", "validated", "surface_map"),
        ("validation_asset_toolpath_data", "validated", "toolpath_data"),
        ("validation_asset_material_profile", "validated", "material_profile"),
    )
