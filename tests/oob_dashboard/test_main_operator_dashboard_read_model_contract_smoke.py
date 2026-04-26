from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)


def test_main_operator_dashboard_read_model_contract_builds() -> None:
    contract = build_main_operator_dashboard_read_model_contract()

    assert len(contract.rows) == 1
    assert contract.rows[0].dashboard_id == "main_operator_dashboard"


def test_main_operator_dashboard_read_model_contract_values() -> None:
    contract = build_main_operator_dashboard_read_model_contract()
    row = contract.rows[0]

    assert row.dashboard_role == "main_operator"
    assert row.primary_workspace_id == "workspace_operator_interaction"
    assert row.secondary_workspace_ids == ("workspace_foundation_monitoring",)
    assert row.total_workspace_count == 2
    assert row.total_panel_count == 8
    assert row.read_only_foundation_reuse is True
    assert row.supports_multimonitor_layout is True
    assert row.supports_voice_gesture_addressing is True
