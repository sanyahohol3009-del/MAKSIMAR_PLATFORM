from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception import (
    build_gesture_backend_adapter_contract,
)


def test_gesture_backend_adapter_contract_is_intent_only() -> None:
    read_model = build_gesture_backend_adapter_contract().to_read_model()

    assert read_model["output_payload_kind"] == "gesture_intent_candidate"
    assert read_model["gesture_intent_candidate_only"] is True
    assert read_model["direct_action_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["always_listening_allowed"] is False
    assert read_model["proposal_only"] is True
