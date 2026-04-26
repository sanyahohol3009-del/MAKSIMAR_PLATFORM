from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_content_contract import (
    ALL_LOGS_PANEL_STATES,
    build_logs_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_payload_builder import (
    build_logs_panel_payload,
)


def test_logs_panel_content_contract_builds() -> None:
    """Logs panel content contract should build successfully."""
    contract = build_logs_panel_content_contract()

    assert contract.contract_id == "logs_panel_content_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1
    assert contract.operator_visible_entries == 1


def test_logs_panel_content_entry_is_canonical() -> None:
    """Logs panel content entry should remain canonical."""
    contract = build_logs_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "logs"
    assert entry.panel_state in ALL_LOGS_PANEL_STATES
    assert entry.total_log_related_entries >= 0
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
    assert entry.operator_visible is True


def test_logs_panel_payload_builder_returns_expected_shape() -> None:
    """Payload builder should return canonical logs payload shape."""
    payload = build_logs_panel_payload()

    assert payload["panel_id"] == "logs"
    assert payload["panel_state"] in ALL_LOGS_PANEL_STATES
    assert "summary" in payload
    assert "severity" in payload
    assert "visibility" in payload


def test_logs_panel_payload_builder_exposes_visibility_semantics() -> None:
    """Payload builder should expose read-only and visibility semantics."""
    payload = build_logs_panel_payload()
    visibility = payload["visibility"]

    assert visibility["visible_in_main_dashboard"] is True
    assert visibility["visible_in_oob_dashboard"] is True
    assert visibility["read_only"] is True
    assert visibility["operator_visible"] is True
