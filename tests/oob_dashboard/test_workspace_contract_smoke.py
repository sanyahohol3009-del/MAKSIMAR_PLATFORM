from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_workspace_contract,
)


def test_workspace_contract_builds() -> None:
    """Workspace contract should build successfully."""
    contract = build_dashboard_workspace_contract()

    assert len(contract.displays) == 3
    assert len(contract.placements) == 7


def test_workspace_contract_has_primary_display() -> None:
    """Workspace contract should include primary display."""
    contract = build_dashboard_workspace_contract()

    display_ids = {display.display_id for display in contract.displays}

    assert 0 in display_ids
