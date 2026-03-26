from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_version_control_panel_contract,
)


def test_version_control_panel_contract_builds() -> None:
    """Version control panel contract should build successfully."""
    contract = build_version_control_panel_contract()

    assert contract.panel_id == "panel_version_control_dashboard"
    assert contract.total_entries == 2
    assert len(contract.entries) == 2


def test_version_control_panel_contains_pending_changes() -> None:
    """Version control panel should expose pending changes state."""
    contract = build_version_control_panel_contract()

    states = {entry.sync_state for entry in contract.entries}

    assert "pending_changes" in states
    assert "clean" in states
