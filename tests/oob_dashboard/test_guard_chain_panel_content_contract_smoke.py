from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract import (
    ALL_GUARD_CHAIN_PANEL_STATES,
    build_guard_chain_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder import (
    build_guard_chain_panel_payload,
)


def test_guard_chain_panel_content_contract_builds() -> None:
    """Guard-chain panel content contract should build successfully."""
    contract = build_guard_chain_panel_content_contract()

    assert contract.contract_id == "guard_chain_panel_content_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1
    assert contract.operator_visible_entries == 1


def test_guard_chain_panel_content_entry_is_canonical() -> None:
    """Guard-chain panel content entry should remain canonical."""
    contract = build_guard_chain_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "guard_chain"
    assert entry.panel_state in ALL_GUARD_CHAIN_PANEL_STATES
    assert entry.total_chain_entries >= 0
    assert entry.runtime_entry_present is True
    assert entry.guard_entry_present is True
    assert entry.core_guard_entry_present is True
    assert entry.kernel_guard_entry_present is True
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
    assert entry.operator_visible is True


def test_guard_chain_panel_payload_builder_returns_expected_shape() -> None:
    """Payload builder should return canonical guard-chain payload shape."""
    payload = build_guard_chain_panel_payload()

    assert payload["panel_id"] == "guard_chain"
    assert payload["panel_state"] in ALL_GUARD_CHAIN_PANEL_STATES
    assert "summary" in payload
    assert "chain_health" in payload
    assert "presence" in payload
    assert "state_context" in payload
    assert "visibility" in payload


def test_guard_chain_panel_payload_builder_exposes_presence_semantics() -> None:
    """Payload builder should expose canonical guard-chain presence semantics."""
    payload = build_guard_chain_panel_payload()
    presence = payload["presence"]

    assert presence["runtime_entry_present"] is True
    assert presence["guard_entry_present"] is True
    assert presence["core_guard_entry_present"] is True
    assert presence["kernel_guard_entry_present"] is True
