from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.queue_load_panel_contract import (
    build_queue_load_panel_contract,
)


def test_queue_load_panel_contract_builds() -> None:
    contract = build_queue_load_panel_contract()

    assert contract.panel_id == "panel_queue_load"
    assert contract.total_entries == 5
    assert contract.operator_visible is True


def test_queue_load_panel_contract_contains_expected_metrics() -> None:
    contract = build_queue_load_panel_contract()

    metrics = tuple((entry.metric_name, entry.metric_value) for entry in contract.entries)

    assert metrics == (
        ("execution_routes", "3"),
        ("lease_count", "0"),
        ("queue_depth", "0"),
        ("load_state", "nominal"),
        ("worker_capacity", "available"),
    )
