from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_contract import (
    build_data_flow_panel_contract,
)


def test_data_flow_panel_contract_builds() -> None:
    contract = build_data_flow_panel_contract()

    assert contract.panel_id == "panel_data_flow"
    assert contract.total_entries == 5
    assert contract.operator_visible is True


def test_data_flow_panel_contract_contains_expected_paths() -> None:
    contract = build_data_flow_panel_contract()

    flow_pairs = tuple(
        (entry.source_component, entry.target_component, entry.flow_class)
        for entry in contract.entries
    )

    assert flow_pairs == (
        ("control_plane", "execution_control", "control_to_execution"),
        ("execution_control", "workers", "execution_to_workers"),
        ("workers", "data_plane", "workers_to_data_plane"),
        ("execution_observability", "oob_dashboard", "observability_projection"),
        ("control_plane", "execution_observability", "control_to_observability"),
    )
