from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_LATENCY_PATH import (
    build_voice_latency_path_contract,
)


def test_voice_latency_path_contract_builds() -> None:
    """Voice latency path contract should build successfully."""
    contract = build_voice_latency_path_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.explanation_required_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_voice_latency_path_contract_contains_expected_memory_path() -> None:
    """Voice latency path should expose expected memory path."""
    contract = build_voice_latency_path_contract()
    entry = contract.entries[0]

    assert entry.path_id == "latencypath_show_memory_001"
    assert entry.intent_id == "intent_show_memory_001"
    assert entry.source_command_id == "voicecmd_show_memory_001"
    assert entry.normalization_binding_id == "intent_show_memory_001"
    assert entry.voice_route_id == "voiceroute_show_memory_001"
    assert entry.display_handoff_id == "voicehandoff_show_memory_001"
    assert entry.execution_handoff_id == "voiceexec_show_memory_001"


def test_voice_latency_path_contract_contains_expected_simulation_path() -> None:
    """Voice latency path should expose expected simulation path."""
    contract = build_voice_latency_path_contract()
    entry = contract.entries[1]

    assert entry.path_id == "latencypath_show_simulation_001"
    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.source_command_id == "voicecmd_show_simulation_001"
    assert entry.normalization_binding_id == "intent_show_simulation_001"
    assert entry.voice_route_id == "voiceroute_show_simulation_001"
    assert entry.display_handoff_id == "voicehandoff_show_simulation_001"
    assert entry.execution_handoff_id == "voiceexec_show_simulation_001"


def test_voice_latency_path_contract_contains_expected_monitoring_path() -> None:
    """Voice latency path should expose expected monitoring path."""
    contract = build_voice_latency_path_contract()
    entry = contract.entries[2]

    assert entry.path_id == "latencypath_show_monitoring_001"
    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.source_command_id == "voicecmd_show_monitoring_001"
    assert entry.normalization_binding_id == "intent_show_monitoring_001"
    assert entry.voice_route_id == "voiceroute_show_monitoring_001"
    assert entry.display_handoff_id == "voicehandoff_show_monitoring_001"
    assert entry.execution_handoff_id == "voiceexec_show_monitoring_001"


def test_voice_latency_path_contract_preserves_stage_order_and_flags() -> None:
    """Voice latency path should preserve canonical stage order and flags."""
    contract = build_voice_latency_path_contract()

    expected_stages = (
        "voice_input_stage",
        "intent_normalization_stage",
        "voice_routing_stage",
        "display_handoff_stage",
        "execution_handoff_stage",
    )

    for entry in contract.entries:
        assert entry.latency_class == "near_instant"
        assert entry.stage_ids == expected_stages
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.multilingual_ready is True
        assert entry.active is True
        assert entry.path_status == "ready"
