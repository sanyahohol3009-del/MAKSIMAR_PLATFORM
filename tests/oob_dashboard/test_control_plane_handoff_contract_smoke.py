from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_control_plane_handoff_contract,
)


def test_control_plane_handoff_contract_builds() -> None:
    """Control-plane handoff contract should build successfully."""
    contract = build_control_plane_handoff_contract()

    assert contract.total_entries == 1
    assert contract.approval_gated_entries == 1
    assert contract.read_only_path_entries == 0


def test_control_plane_handoff_entry() -> None:
    """Control-plane handoff entry should remain canonical."""
    contract = build_control_plane_handoff_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.handoff_target == "control_plane_router"
    assert entry.handoff_status == "handoff_only"
    assert entry.handoff_mode == "approval_gated"
    assert entry.direct_execution_allowed is False
