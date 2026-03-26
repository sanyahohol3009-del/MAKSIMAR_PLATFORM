from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_queue_load_panel_contract,
)


def test_queue_load_panel_contract_builds() -> None:
    """Queue/load panel contract should build successfully."""
    contract = build_queue_load_panel_contract()

    assert contract.panel_id == "panel_queue_load"
    assert contract.total_entries == 5
    assert len(contract.entries) == 5


def test_queue_load_panel_contains_execution_routes() -> None:
    """Queue/load panel should expose execution routes metric."""
    contract = build_queue_load_panel_contract()

    metric_names = {entry.metric_name for entry in contract.entries}

    assert "execution_routes" in metric_names
    assert "lease_count" in metric_names
