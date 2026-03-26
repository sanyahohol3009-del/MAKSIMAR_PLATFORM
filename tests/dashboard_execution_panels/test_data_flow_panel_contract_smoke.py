from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_data_flow_panel_contract,
)


def test_data_flow_panel_contract_builds() -> None:
    """Data flow panel contract should build successfully."""
    contract = build_data_flow_panel_contract()

    assert contract.panel_id == "panel_data_flow"
    assert contract.total_entries == 5
    assert len(contract.entries) == 5


def test_data_flow_panel_contains_execution_path() -> None:
    """Data flow panel should expose control_plane to execution_control path."""
    contract = build_data_flow_panel_contract()

    pairs = {
        (entry.source_component, entry.target_component)
        for entry in contract.entries
    }

    assert ("control_plane", "execution_control") in pairs
    assert ("execution_control", "workers") in pairs
