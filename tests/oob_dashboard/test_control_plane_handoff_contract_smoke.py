from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_control_plane_handoff_contract,
)


def test_control_plane_handoff_contract_builds() -> None:
    """Control-plane handoff contract should build successfully."""
    contract = build_control_plane_handoff_contract()

    assert contract.total_entries == 3
    assert contract.approval_gated_entries == 1
    assert contract.read_only_path_entries == 2


def test_control_plane_handoff_contract_contains_expected_entries() -> None:
    """Control-plane handoff contract should contain expected canonical entries."""
    contract = build_control_plane_handoff_contract()

    read_only_entries = [
        entry for entry in contract.entries if entry.handoff_mode == "read_only_path"
    ]
    approval_gated_entries = [
        entry for entry in contract.entries if entry.handoff_mode == "approval_gated"
    ]

    assert len(read_only_entries) == 2
    assert len(approval_gated_entries) == 1

    for entry in contract.entries:
        assert entry.dashboard_id == "dashboard_main_operator_001"
        assert entry.workspace_id == "workspace_operator_main"
        assert entry.handoff_target == "control_plane_router"
        assert entry.handoff_status == "handoff_only"
        assert entry.direct_execution_allowed is False

    control_entry = approval_gated_entries[0]
    assert control_entry.handoff_mode == "approval_gated"
