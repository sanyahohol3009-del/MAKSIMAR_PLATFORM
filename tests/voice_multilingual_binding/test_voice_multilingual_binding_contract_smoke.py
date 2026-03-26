from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_MULTILINGUAL_BINDING import (
    build_voice_multilingual_binding_contract,
)


def test_voice_multilingual_binding_contract_builds() -> None:
    """Voice multilingual binding contract should build successfully."""
    contract = build_voice_multilingual_binding_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.multilingual_ready_entries == 3
    assert contract.multiscript_ready_entries == 3


def test_voice_multilingual_binding_contract_contains_expected_memory_binding() -> None:
    """Voice multilingual binding should expose expected memory binding."""
    contract = build_voice_multilingual_binding_contract()
    entry = contract.entries[0]

    assert entry.binding_id == "voicemlang_show_memory_001"
    assert entry.intent_id == "intent_show_memory_001"
    assert entry.voice_route_id == "voiceroute_show_memory_001"
    assert entry.latency_path_id == "latencypath_show_memory_001"
    assert entry.canonical_text == "show memory"
    assert entry.localized_texts == (
        "show memory",
        "покажи память",
        "покажи памʼять",
        "zeige speicher",
    )


def test_voice_multilingual_binding_contract_contains_expected_simulation_binding() -> None:
    """Voice multilingual binding should expose expected simulation binding."""
    contract = build_voice_multilingual_binding_contract()
    entry = contract.entries[1]

    assert entry.binding_id == "voicemlang_show_simulation_001"
    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.voice_route_id == "voiceroute_show_simulation_001"
    assert entry.latency_path_id == "latencypath_show_simulation_001"
    assert entry.canonical_text == "show simulation"
    assert entry.localized_texts == (
        "show simulation",
        "покажи симуляцию",
        "покажи симуляцію",
        "zeige simulation",
    )


def test_voice_multilingual_binding_contract_contains_expected_monitoring_binding() -> None:
    """Voice multilingual binding should expose expected monitoring binding."""
    contract = build_voice_multilingual_binding_contract()
    entry = contract.entries[2]

    assert entry.binding_id == "voicemlang_show_monitoring_001"
    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.voice_route_id == "voiceroute_show_monitoring_001"
    assert entry.latency_path_id == "latencypath_show_monitoring_001"
    assert entry.canonical_text == "show monitoring"
    assert entry.localized_texts == (
        "show monitoring",
        "покажи мониторинг",
        "покажи моніторинг",
        "zeige monitoring",
    )


def test_voice_multilingual_binding_contract_preserves_language_and_script_sets() -> None:
    """Voice multilingual binding should preserve canonical language and script sets."""
    contract = build_voice_multilingual_binding_contract()

    for entry in contract.entries:
        assert entry.supported_languages == ("en", "ru", "uk", "de")
        assert entry.supported_scripts == ("Latin", "Cyrillic")
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.multilingual_ready is True
        assert entry.multiscript_ready is True
        assert entry.active is True
        assert entry.binding_status == "bound"
