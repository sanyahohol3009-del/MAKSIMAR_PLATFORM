from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract import (
    ALL_SYSTEM_STATUS_PANEL_STATES,
    build_system_status_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_payload_builder import (
    build_system_status_panel_payload,
)


def test_system_status_panel_content_contract_builds() -> None:
    """System-status panel content contract should build successfully."""
    contract = build_system_status_panel_content_contract()

    assert contract.contract_id == "system_status_panel_content_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1
    assert contract.operator_visible_entries == 1


def test_system_status_panel_content_entry_is_canonical() -> None:
    """System-status panel content entry should remain canonical."""
    contract = build_system_status_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "system_status"
    assert entry.panel_state in ALL_SYSTEM_STATUS_PANEL_STATES
    assert entry.total_foundation_panels >= 0
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
    assert entry.operator_visible is True


def test_system_status_panel_payload_builder_returns_expected_shape() -> None:
    """Payload builder should return canonical system-status payload shape."""
    payload = build_system_status_panel_payload()

    assert payload["panel_id"] == "system_status"
    assert payload["panel_state"] in ALL_SYSTEM_STATUS_PANEL_STATES
    assert "summary" in payload
    assert "truth" in payload
    assert "live_historical" in payload
    assert "visibility" in payload


def test_system_status_panel_payload_builder_exposes_visibility_semantics() -> None:
    """Payload builder should expose read-only and visibility semantics."""
    payload = build_system_status_panel_payload()
    visibility = payload["visibility"]

    assert visibility["visible_in_main_dashboard"] is True
    assert visibility["visible_in_oob_dashboard"] is True
    assert visibility["read_only"] is True
    assert visibility["operator_visible"] is True
