from __future__ import annotations

from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_text_loop_adapter_contract import (
    build_jarvis_live_text_loop_adapter_contract,
)


def test_jarvis_live_text_loop_adapter_is_read_only_smoke_path() -> None:
    read_model = build_jarvis_live_text_loop_adapter_contract().to_read_model()

    assert read_model["text_input_allowed"] is True
    assert read_model["llm_answer_allowed"] is True
    assert read_model["qwen_model_available"] is True
    assert read_model["qwen_probe_passed"] is True
    assert read_model["tts_output_allowed"] is True
    assert read_model["project_context_reader_required"] is True
    assert read_model["shell_allowed"] is False
    assert read_model["file_edit_allowed"] is False
    assert read_model["git_allowed"] is False
    assert read_model["app_control_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["autonomous_loop_allowed"] is False
    assert read_model["microphone_allowed"] is False
    assert read_model["stt_allowed"] is False
    assert read_model["wake_word_allowed"] is False
    assert read_model["owner_command_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["audit_required"] is True
    assert read_model["preview_required"] is True

