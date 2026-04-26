from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (
    build_preview_surface_contract,
)


def test_preview_surface_contract_builds() -> None:
    """Preview surface contract should build successfully."""
    contract = build_preview_surface_contract()

    assert contract.contract_id == "preview_surface_contract_001"
    assert contract.total_entries == 8
    assert contract.foundation_preview_entries == 5
    assert contract.interaction_preview_entries == 3
    assert contract.panel_preview_generation_entries == 5
    assert contract.fixture_preview_generation_entries == 3
    assert contract.operator_visible_entries == 8


def test_preview_surface_contract_contains_expected_entries() -> None:
    """Preview surface contract should contain expected canonical entries."""
    contract = build_preview_surface_contract()
    entry_map = {entry.panel_id: entry for entry in contract.entries}

    assert entry_map["system_status"].preview_surface_class == "foundation_preview_surface"
    assert entry_map["system_status"].preview_generation_mode == "panel_preview_generation"

    assert entry_map["action_queue"].preview_surface_class == "interaction_preview_surface"
    assert entry_map["action_queue"].preview_generation_mode == "fixture_preview_generation"

    assert entry_map["approval_queue"].preview_surface_class == "interaction_preview_surface"
    assert entry_map["audit_timeline"].preview_surface_class == "interaction_preview_surface"

    assert entry_map["system_status"].visible_in_navigation is True
    assert entry_map["action_queue"].visible_in_main_dashboard is True
