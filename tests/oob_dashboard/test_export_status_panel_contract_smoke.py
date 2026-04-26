from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.export_status_panel_contract import (
    build_export_status_panel_contract,
)


def test_export_status_panel_contract_builds() -> None:
    contract = build_export_status_panel_contract()

    assert contract.panel_id == "panel_export_status"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_export_status_panel_contract_contains_expected_entries() -> None:
    contract = build_export_status_panel_contract()

    states = tuple(
        (entry.export_target_id, entry.export_state, entry.artifact_kind)
        for entry in contract.entries
    )

    assert states == (
        ("project_snapshot_bundle", "ready_for_export", "snapshot_bundle"),
        ("validation_report_bundle", "ready_for_export", "validation_report"),
        ("preview_render_bundle", "ready_for_export", "preview_render"),
    )
