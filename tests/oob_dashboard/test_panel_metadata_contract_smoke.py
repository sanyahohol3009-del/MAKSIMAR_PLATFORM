from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_metadata_contract,
)


def test_panel_metadata_contract_builds() -> None:
    """Panel metadata contract should build successfully."""
    contract = build_panel_metadata_contract()

    assert contract.total_entries == 19
    assert contract.read_only_entries == 15
    assert contract.interactive_controlled_entries == 1
    assert contract.interactive_restricted_entries == 2
    assert contract.hidden_internal_entries == 1


def test_panel_metadata_foundation_runtime_entry() -> None:
    """Foundation runtime metadata should be canonical."""
    contract = build_panel_metadata_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.display_title == "Runtime Core"
    assert entry.priority == 1
    assert entry.source_domain == "foundation"
    assert entry.read_mode == "read_only"
    assert entry.panel_state_class == "foundation"


def test_panel_metadata_chat_entry() -> None:
    """Chat metadata should remain controlled interactive."""
    contract = build_panel_metadata_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.display_title == "Chat"
    assert entry.read_mode == "interactive_controlled"
    assert entry.panel_state_class == "operator"
    assert entry.source_domain == "interaction"


def test_panel_metadata_navigation_entry() -> None:
    """Navigation metadata should stay hidden internal."""
    contract = build_panel_metadata_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.read_mode == "hidden_internal"
    assert entry.panel_state_class == "operator"
    assert entry.source_domain == "navigation"
