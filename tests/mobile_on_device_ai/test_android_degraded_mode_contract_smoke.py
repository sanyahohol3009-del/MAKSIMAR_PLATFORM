from __future__ import annotations

from ANDROID_SHELL.local_ai_runtime.android_degraded_mode_contract import (
    build_android_degraded_mode_contract,
)


def test_android_degraded_mode_contract_is_safe_text_only() -> None:
    read_model = build_android_degraded_mode_contract().to_read_model()

    assert read_model["platform"] == "android"
    assert read_model["degraded_mode_available"] is True
    assert read_model["degraded_mode_is_app_safe"] is True
    assert read_model["degraded_mode_text_intent_only"] is True
    assert read_model["degraded_mode_can_answer_local_safe_help"] is True
    assert read_model["degraded_mode_can_execute_core_actions"] is False
    assert read_model["degraded_mode_can_write_memory"] is False
    assert read_model["degraded_mode_can_control_phone"] is False
    assert read_model["degraded_mode_can_control_pc"] is False
    assert read_model["degraded_mode_can_bypass_approval"] is False
    assert read_model["degraded_mode_requires_server_resync"] is True
    assert read_model["proposal_only"] is True
