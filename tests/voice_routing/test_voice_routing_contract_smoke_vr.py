from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_ROUTING import (
    build_voice_routing_contract,
)


def test_voice_routing_contract_builds() -> None:
    """Voice routing contract should build successfully."""
    contract = build_voice_routing_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.explanation_required_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_voice_routing_contract_contains_expected_memory_route() -> None:
    """Voice routing contract should expose expected memory route."""
    contract = build_voice_routing_contract()
    entry = contract.entries[0]

    assert entry.voice_route_id == "voiceroute_show_memory_001"
    assert entry.intent_id == "intent_show_memory_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_memory_001"
    assert entry.command_intent == "show_memory"
    assert entry.target_display_route_id == "displayroute_show_memory_001"
    assert entry.target_view_id == "view_memory_project_architecture"
    assert entry.target_display_role == "mobile_display_proxy"
    assert entry.target_panel_id == "panel_memory_project_architecture"


def test_voice_routing_contract_contains_expected_simulation_route() -> None:
    """Voice routing contract should expose expected simulation route."""
    contract = build_voice_routing_contract()
    entry = contract.entries[1]

    assert entry.voice_route_id == "voiceroute_show_simulation_001"
    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_simulation_001"
    assert entry.command_intent == "show_simulation"
    assert entry.target_display_route_id == "displayroute_show_simulation_001"
    assert entry.target_view_id == "view_simulation_skill_overview"
    assert entry.target_display_role == "engineering_display"
    assert entry.target_panel_id == "panel_simulation_skill_overview"


def test_voice_routing_contract_contains_expected_monitoring_route() -> None:
    """Voice routing contract should expose expected monitoring route."""
    contract = build_voice_routing_contract()
    entry = contract.entries[2]

    assert entry.voice_route_id == "voiceroute_show_monitoring_001"
    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.intent_source == "voice"
    assert entry.source_command_id == "voicecmd_show_monitoring_001"
    assert entry.command_intent == "show_monitoring"
    assert entry.target_display_route_id == "displayroute_show_monitoring_001"
    assert entry.target_view_id == "view_monitoring_panel"
    assert entry.target_display_role == "primary_dashboard_display"
    assert entry.target_panel_id == "panel_monitoring_panel"


def test_voice_routing_contract_preserves_low_latency_and_explanation_flags() -> None:
    """Voice routing contract should preserve low-latency and explanation semantics."""
    contract = build_voice_routing_contract()

    for entry in contract.entries:
        assert entry.routing_mode == "normalized_intent_to_display_route"
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.multilingual_ready is True
        assert entry.active is True
        assert entry.route_status == "bound"
