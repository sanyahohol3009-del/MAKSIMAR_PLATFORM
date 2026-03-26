from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_project_map_panel_contract,
)


def test_project_map_panel_contract_builds() -> None:
    """Project map panel contract should build successfully."""
    contract = build_project_map_panel_contract()

    assert contract.panel_id == "panel_project_map"
    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_project_map_panel_contains_execution_control() -> None:
    """Project map panel should expose execution_control module."""
    contract = build_project_map_panel_contract()

    module_ids = {entry.module_id for entry in contract.entries}

    assert "control_plane" in module_ids
    assert "execution_control" in module_ids
