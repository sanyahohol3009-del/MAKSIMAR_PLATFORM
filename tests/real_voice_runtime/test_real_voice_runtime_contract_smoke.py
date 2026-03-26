from __future__ import annotations

from MAKSIMAR_CORE_LIB.real_voice_runtime import (
    build_real_voice_runtime_contract,
)


def test_real_voice_runtime_contract_builds() -> None:
    """Real voice runtime contract should build successfully."""
    contract = build_real_voice_runtime_contract()

    assert contract.total_entries == 3
    assert contract.display_runtime_entries == 2
    assert contract.execution_runtime_entries == 1
    assert contract.multilingual_entries == 3
    assert contract.active_entries == 3


def test_real_voice_runtime_contract_contains_expected_memory_entry() -> None:
    """Real voice runtime should expose expected memory entry."""
    contract = build_real_voice_runtime_contract()
    entry = contract.entries[0]

    assert entry.real_voice_runtime_entry_id == "realvoice_show_memory_001"
    assert entry.linked_voice_command_id == "voicecmd_show_memory_001"
    assert entry.linked_intent_id == "intent_show_memory_001"
    assert entry.linked_orchestration_entry_id == "orchestration_mobile_entry_001"
    assert entry.voice_runtime_mode == "display_runtime"


def test_real_voice_runtime_contract_contains_expected_simulation_entry() -> None:
    """Real voice runtime should expose expected simulation entry."""
    contract = build_real_voice_runtime_contract()
    entry = contract.entries[1]

    assert entry.real_voice_runtime_entry_id == "realvoice_show_simulation_001"
    assert entry.linked_voice_command_id == "voicecmd_show_simulation_001"
    assert entry.linked_intent_id == "intent_show_simulation_001"
    assert entry.linked_orchestration_entry_id == "orchestration_heavy_execution_001"
    assert entry.voice_runtime_mode == "execution_runtime"


def test_real_voice_runtime_contract_contains_expected_monitoring_entry() -> None:
    """Real voice runtime should expose expected monitoring entry."""
    contract = build_real_voice_runtime_contract()
    entry = contract.entries[2]

    assert entry.real_voice_runtime_entry_id == "realvoice_show_monitoring_001"
    assert entry.linked_voice_command_id == "voicecmd_show_monitoring_001"
    assert entry.linked_intent_id == "intent_show_monitoring_001"
    assert entry.linked_orchestration_entry_id == "orchestration_control_plane_001"
    assert entry.voice_runtime_mode == "display_runtime"
