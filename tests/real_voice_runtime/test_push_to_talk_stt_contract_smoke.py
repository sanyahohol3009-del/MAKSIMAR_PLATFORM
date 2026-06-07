from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.real_voice_runtime.push_to_talk_stt_contract import (
    PushToTalkSttContract,
    build_push_to_talk_stt_contract,
)


def test_push_to_talk_stt_contract_allows_only_manual_owner_activation() -> None:
    read_model = build_push_to_talk_stt_contract().to_read_model()

    assert read_model["push_to_talk_allowed"] is True
    assert read_model["manual_activation_required"] is True
    assert read_model["microphone_permission_required"] is True
    assert read_model["physical_mic_kill_switch_supported"] is True
    assert read_model["future_always_listening_requested"] is True
    assert read_model["future_always_listening_requires_owner_voice_gate"] is True
    assert read_model["future_always_listening_requires_local_vad"] is True
    assert read_model["future_always_listening_requires_visible_status"] is True
    assert read_model["future_always_listening_requires_physical_kill_switch"] is True
    assert read_model["future_always_listening_requires_audit"] is True
    assert read_model["always_listening_allowed"] is False
    assert read_model["wake_word_allowed"] is False
    assert read_model["background_recording_allowed"] is False
    assert read_model["hidden_recording_allowed"] is False
    assert read_model["autonomous_voice_loop_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["shell_allowed"] is False
    assert read_model["file_edit_allowed"] is False
    assert read_model["git_allowed"] is False


def test_push_to_talk_stt_contract_rejects_dangerous_true_flags() -> None:
    with pytest.raises(ValueError, match="must remain disabled"):
        PushToTalkSttContract(
            contract_id="push_to_talk_stt_contract_v0_1",
            always_listening_allowed=True,
        )
    with pytest.raises(ValueError, match="must remain disabled"):
        PushToTalkSttContract(
            contract_id="push_to_talk_stt_contract_v0_1",
            wake_word_allowed=True,
        )

