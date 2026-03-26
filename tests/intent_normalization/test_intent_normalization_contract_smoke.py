from __future__ import annotations

from MAKSIMAR_SERVER.INTENT_NORMALIZATION import (
    build_intent_normalization_contract,
)


def test_intent_normalization_contract_builds() -> None:
    """Intent normalization contract should build successfully."""
    contract = build_intent_normalization_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.explanation_required_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_intent_normalization_contract_contains_expected_memory_intent() -> None:
    """Intent normalization contract should expose expected memory intent."""
    contract = build_intent_normalization_contract()
    entry = contract.entries[0]

    assert entry.intent_id == "intent_show_memory_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_memory_001"
    assert entry.intent_kind == "display_request"
    assert entry.target_domain == "memory"
    assert entry.target_action == "show"
    assert entry.target_view_id == "view_memory_project_architecture"
    assert entry.target_display_role == "mobile_display_proxy"
    assert entry.normalized_text == "show memory"


def test_intent_normalization_contract_contains_expected_simulation_intent() -> None:
    """Intent normalization contract should expose expected simulation intent."""
    contract = build_intent_normalization_contract()
    entry = contract.entries[1]

    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_simulation_001"
    assert entry.target_domain == "simulation"
    assert entry.target_view_id == "view_simulation_skill_overview"
    assert entry.target_display_role == "engineering_display"
    assert entry.normalized_text == "show simulation"


def test_intent_normalization_contract_contains_expected_monitoring_intent() -> None:
    """Intent normalization contract should expose expected monitoring intent."""
    contract = build_intent_normalization_contract()
    entry = contract.entries[2]

    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_monitoring_001"
    assert entry.target_domain == "monitoring"
    assert entry.target_view_id == "view_monitoring_panel"
    assert entry.target_display_role == "primary_dashboard_display"
    assert entry.normalized_text == "show monitoring"


def test_intent_normalization_contract_preserves_flags() -> None:
    """Intent normalization contract should preserve platform flags."""
    contract = build_intent_normalization_contract()

    for entry in contract.entries:
        assert entry.confidence_band == "high"
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.multilingual_ready is True
        assert entry.active is True
        assert entry.normalization_status == "normalized"
