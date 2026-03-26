from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_layer import (
    build_voice_command_contract,
)


def test_voice_command_contract_builds() -> None:
    """Voice command contract should build successfully."""
    contract = build_voice_command_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_voice_command_contract_contains_expected_memory_command() -> None:
    """Voice command contract should expose expected memory command."""
    contract = build_voice_command_contract()
    entry = contract.entries[0]

    assert entry.command_id == "voicecmd_show_memory_001"
    assert entry.utterance_pattern_id == "utterance_show_memory_001"
    assert entry.command_intent == "show_memory"
    assert entry.target_view_id == "view_memory_project_architecture"
    assert entry.target_display_route_id == "displayroute_show_memory_001"
    assert entry.target_display_role == "mobile_display_proxy"


def test_voice_command_contract_contains_expected_simulation_command() -> None:
    """Voice command contract should expose expected simulation command."""
    contract = build_voice_command_contract()
    entry = contract.entries[1]

    assert entry.command_id == "voicecmd_show_simulation_001"
    assert entry.utterance_pattern_id == "utterance_show_simulation_001"
    assert entry.command_intent == "show_simulation"
    assert entry.target_view_id == "view_simulation_skill_overview"
    assert entry.target_display_route_id == "displayroute_show_simulation_001"
    assert entry.target_display_role == "engineering_display"


def test_voice_command_contract_contains_expected_monitoring_command() -> None:
    """Voice command contract should expose expected monitoring command."""
    contract = build_voice_command_contract()
    entry = contract.entries[2]

    assert entry.command_id == "voicecmd_show_monitoring_001"
    assert entry.utterance_pattern_id == "utterance_show_monitoring_001"
    assert entry.command_intent == "show_monitoring"
    assert entry.target_view_id == "view_monitoring_panel"
    assert entry.target_display_route_id == "displayroute_show_monitoring_001"
    assert entry.target_display_role == "primary_dashboard_display"


def test_voice_command_contract_preserves_low_latency_and_multilingual_flags() -> None:
    """Voice command contract should preserve low-latency and multilingual semantics."""
    contract = build_voice_command_contract()

    for entry in contract.entries:
        assert entry.response_mode == "voice_plus_display"
        assert entry.latency_class == "near_instant"
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.multilingual_ready is True
        assert entry.supported_languages == ("en", "ru", "uk", "de")
        assert entry.supported_scripts == ("Latin", "Cyrillic")
        assert entry.active is True
