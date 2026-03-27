from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_source_binding_contract,
)


def test_panel_source_binding_contract_builds() -> None:
    """Panel source binding contract should build successfully."""
    contract = build_panel_source_binding_contract()

    assert contract.total_entries == 19
    assert contract.read_only_entries == 16
    assert contract.mutable_entries == 3


def test_panel_source_binding_foundation_runtime_entry() -> None:
    """Foundation runtime panel should bind to canonical summary source."""
    contract = build_panel_source_binding_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.source_binding == "foundation_status_summary_contract"
    assert entry.source_contract_name == "build_foundation_status_panel_summary_contract"
    assert entry.source_scope == "foundation"
    assert entry.read_only is True


def test_panel_source_binding_chat_entry() -> None:
    """Chat panel should remain controlled non-read-only source."""
    contract = build_panel_source_binding_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.source_binding == "dashboard_chat_contract"
    assert entry.source_contract_name == "build_dashboard_chat_contract"
    assert entry.source_scope == "interaction"
    assert entry.read_only is False


def test_panel_source_binding_gesture_entry() -> None:
    """Gesture panel should bind to canonical gesture contract."""
    contract = build_panel_source_binding_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_gesture_control"
    )

    assert entry.source_binding == "gesture_panel_contract"
    assert entry.source_contract_name == "build_dashboard_gesture_panel"
    assert entry.source_scope == "control"
    assert entry.read_only is False
