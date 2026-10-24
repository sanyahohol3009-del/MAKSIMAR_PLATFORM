from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_DISPLAY_HANDOFF import (
    build_voice_display_handoff_contract,
)


def test_voice_display_handoff_contract_builds() -> None:
    """Voice display handoff contract should build successfully."""
    contract = build_voice_display_handoff_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.explanation_ready_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_voice_display_handoff_contract_contains_expected_memory_handoff() -> None:
    """Voice display handoff should expose expected memory handoff."""
    contract = build_voice_display_handoff_contract()
    entry = contract.entries[0]

    assert entry.handoff_id == "voicehandoff_show_memory_001"
    assert entry.voice_route_id == "voiceroute_show_memory_001"
    assert entry.intent_id == "intent_show_memory_001"
    assert entry.display_route_id == "displayroute_show_memory_001"
    assert entry.target_view_id == "view_memory_project_architecture"
    assert entry.target_display_id == "display_mobile_proxy_001"
    assert entry.target_display_role == "mobile_display_proxy"
    assert entry.target_panel_id == "panel_memory_project_architecture"


def test_voice_display_handoff_contract_contains_expected_simulation_handoff() -> None:
    """Voice display handoff should expose expected simulation handoff."""
    contract = build_voice_display_handoff_contract()
    entry = contract.entries[1]

    assert entry.handoff_id == "voicehandoff_show_simulation_001"
    assert entry.voice_route_id == "voiceroute_show_simulation_001"
    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.display_route_id == "displayroute_show_simulation_001"
    assert entry.target_view_id == "view_simulation_skill_overview"
    assert entry.target_display_id == "display_engineering_001"
    assert entry.target_display_role == "engineering_display"
    assert entry.target_panel_id == "panel_simulation_skill_overview"


def test_voice_display_handoff_contract_contains_expected_monitoring_handoff() -> None:
    """Voice display handoff should expose expected monitoring handoff."""
    contract = build_voice_display_handoff_contract()
    entry = contract.entries[2]

    assert entry.handoff_id == "voicehandoff_show_monitoring_001"
    assert entry.voice_route_id == "voiceroute_show_monitoring_001"
    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.display_route_id == "displayroute_show_monitoring_001"
    assert entry.target_view_id == "view_monitoring_panel"
    assert entry.target_display_id == "display_primary_dashboard_001"
    assert entry.target_display_role == "primary_dashboard_display"
    assert entry.target_panel_id == "panel_monitoring_panel"


def test_voice_display_handoff_contract_preserves_explanation_and_latency_flags() -> None:
    """Voice display handoff should preserve explanation and latency semantics."""
    contract = build_voice_display_handoff_contract()

    for entry in contract.entries:
        assert entry.handoff_mode == "display_plus_explanation"
        assert entry.low_latency_required is True
        assert entry.explanation_text_available is True
        assert entry.explanation_payload_available is True
        assert entry.multilingual_ready is True
        assert entry.active is True
        assert entry.handoff_status == "ready"
