from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception import (
    build_perception_policy_contract,
)


def test_perception_policy_contract_keeps_phase_8_boundaries_closed() -> None:
    read_model = build_perception_policy_contract().to_read_model()

    assert read_model["raw_audio_blocked_by_default"] is True
    assert read_model["text_intent_only"] is True
    assert read_model["action_execution_allowed"] is False
    assert read_model["approval_required_for_actions"] is True
    assert read_model["proposal_only"] is True
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["PHASE_9_JUNIOR_MODEL_PARKED"] is True
    assert read_model["WINDOWS_VOICE_EDGE_PARKED"] is True
    assert read_model["PUSH_TO_TALK_STT_LIVE_PARKED"] is True
    assert read_model["junior_mobile_runtime_enabled"] is False
    assert read_model["local_mobile_model_enabled"] is False
    assert read_model["local_inference_allowed"] is False
