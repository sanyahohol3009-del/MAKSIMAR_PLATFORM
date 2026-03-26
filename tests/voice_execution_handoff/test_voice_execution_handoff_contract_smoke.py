from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_EXECUTION_HANDOFF import (
    build_voice_execution_handoff_contract,
)


def test_voice_execution_handoff_contract_builds() -> None:
    """Voice execution handoff contract should build successfully."""
    contract = build_voice_execution_handoff_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.low_latency_entries == 3
    assert contract.policy_compatible_entries == 3
    assert contract.ready_entries == 3


def test_voice_execution_handoff_contract_contains_expected_memory_entry() -> None:
    """Voice execution handoff should expose expected memory entry."""
    contract = build_voice_execution_handoff_contract()
    entry = contract.entries[0]

    assert entry.handoff_id == "voiceexec_show_memory_001"
    assert entry.intent_id == "intent_show_memory_001"
    assert entry.display_handoff_id == "voicehandoff_show_memory_001"
    assert entry.intent_kind == "display_request"
    assert entry.task_class == "chat_request"
    assert entry.payload_class == "small_control"
    assert entry.policy_rule_id == "policy_chat_request_small_control"
    assert entry.validation_request_id == "valreq_show_memory_001"


def test_voice_execution_handoff_contract_contains_expected_simulation_entry() -> None:
    """Voice execution handoff should expose expected simulation entry."""
    contract = build_voice_execution_handoff_contract()
    entry = contract.entries[1]

    assert entry.handoff_id == "voiceexec_show_simulation_001"
    assert entry.intent_id == "intent_show_simulation_001"
    assert entry.display_handoff_id == "voicehandoff_show_simulation_001"
    assert entry.intent_kind == "display_request"
    assert entry.task_class == "simulation_request"
    assert entry.payload_class == "small_control"
    assert entry.policy_rule_id == "policy_simulation_request_small_control"
    assert entry.validation_request_id == "valreq_show_simulation_001"


def test_voice_execution_handoff_contract_contains_expected_monitoring_entry() -> None:
    """Voice execution handoff should expose expected monitoring entry."""
    contract = build_voice_execution_handoff_contract()
    entry = contract.entries[2]

    assert entry.handoff_id == "voiceexec_show_monitoring_001"
    assert entry.intent_id == "intent_show_monitoring_001"
    assert entry.display_handoff_id == "voicehandoff_show_monitoring_001"
    assert entry.intent_kind == "display_request"
    assert entry.task_class == "chat_request"
    assert entry.payload_class == "small_control"
    assert entry.policy_rule_id == "policy_chat_request_small_control"
    assert entry.validation_request_id == "valreq_show_monitoring_001"


def test_voice_execution_handoff_contract_preserves_policy_and_latency_flags() -> None:
    """Voice execution handoff should preserve policy and latency semantics."""
    contract = build_voice_execution_handoff_contract()

    for entry in contract.entries:
        assert entry.resolved_validation_tier == "L1_HEADER"
        assert entry.admission_decision == "accept"
        assert entry.pressure_level == "normal"
        assert entry.low_latency_required is True
        assert entry.explanation_required is True
        assert entry.policy_compatible is True
        assert entry.active is True
        assert entry.handoff_mode == "validation_policy_admission_handoff"
        assert entry.handoff_status == "ready"
