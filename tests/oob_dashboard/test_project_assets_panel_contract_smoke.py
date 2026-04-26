from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.project_assets_panel_contract import (
    build_project_assets_panel_contract,
)


def test_project_assets_panel_contract_builds() -> None:
    contract = build_project_assets_panel_contract()

    assert contract.panel_id == "panel_project_assets"
    assert contract.total_entries == 3
    assert contract.ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_project_assets_panel_contract_contains_expected_entries() -> None:
    contract = build_project_assets_panel_contract()

    states = tuple(
        (entry.project_asset_id, entry.asset_state, entry.asset_kind)
        for entry in contract.entries
    )

    assert states == (
        ("project_asset_description_txt", "ready", "description_file"),
        ("project_asset_system_overview_md", "ready", "system_overview"),
        ("project_asset_preview_render_png", "ready", "preview_render"),
    )
