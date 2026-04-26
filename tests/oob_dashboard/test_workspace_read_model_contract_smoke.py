from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_contract import (
    build_workspace_read_model_contract,
)


def test_workspace_read_model_contract_builds() -> None:
    contract = build_workspace_read_model_contract()

    assert len(contract.rows) == 2
    assert contract.rows[0].workspace_id == "workspace_foundation_monitoring"
    assert contract.rows[1].workspace_id == "workspace_operator_interaction"


def test_workspace_read_model_contract_values() -> None:
    contract = build_workspace_read_model_contract()
    row_map = {row.workspace_id: row for row in contract.rows}

    foundation_row = row_map["workspace_foundation_monitoring"]
    assert foundation_row.panel_count == 5
    assert foundation_row.panel_ids == (
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    )

    operator_row = row_map["workspace_operator_interaction"]
    assert operator_row.panel_count == 3
    assert operator_row.panel_ids == (
        "action_queue",
        "approval_queue",
        "audit_timeline",
    )
