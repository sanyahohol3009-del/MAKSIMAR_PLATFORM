from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.voice_perception.voice_perception_status_read_model import (
    build_voice_perception_status_read_model,
)


def test_phase_8_acceptance_artifacts_and_markers_exist() -> None:
    root = Path(__file__).resolve().parents[2]

    required_files = (
        "MAKSIMAR_CORE_LIB/voice_perception/__init__.py",
        "MAKSIMAR_CORE_LIB/voice_perception/asr_backend_adapter_contract.py",
        "MAKSIMAR_CORE_LIB/voice_perception/voice_clone_backend_adapter_contract.py",
        "MAKSIMAR_CORE_LIB/voice_perception/gesture_backend_adapter_contract.py",
        "MAKSIMAR_CORE_LIB/voice_perception/perception_policy_contract.py",
        "ANDROID_SHELL/voice_adapter/moonshine_android_adapter_contract.py",
        "ANDROID_SHELL/voice_adapter/mediapipe_android_adapter_contract.py",
        "ANDROID_SHELL/voice_adapter/android_voice_state_bridge.py",
        "IOS_SHELL/voice_adapter/moonshine_ios_adapter_contract.py",
        "IOS_SHELL/voice_adapter/mediapipe_ios_adapter_contract.py",
        "IOS_SHELL/voice_adapter/ios_voice_state_bridge.py",
        "MAKSIMAR_CORE_LIB/voice_perception/voice_perception_status_read_model.py",
        "tools/voice_perception_status_preview.py",
        "CONTAINER_DEPLOYMENT/cubes/voice_perception/container_contract.yaml",
        "docs/architecture/voice_perception/phase_8_voice_perception_acceptance_v1.md",
    )
    required_tests = (
        "tests/voice_perception/test_asr_backend_adapter_contract_smoke.py",
        "tests/voice_perception/test_voice_clone_backend_adapter_contract_smoke.py",
        "tests/voice_perception/test_gesture_backend_adapter_contract_smoke.py",
        "tests/voice_perception/test_voice_ownership_still_required_smoke.py",
        "tests/voice_perception/test_perception_policy_contract_smoke.py",
        "tests/voice_perception/test_android_voice_state_bridge_smoke.py",
        "tests/voice_perception/test_ios_voice_state_bridge_smoke.py",
        "tests/voice_perception/test_local_asr_sends_text_only_smoke.py",
        "tests/voice_perception/test_raw_audio_stream_blocked_by_default_smoke.py",
        "tests/voice_perception/test_voice_perception_status_read_model_smoke.py",
        "tests/voice_perception/test_voice_message_allowed_as_chat_attachment_smoke.py",
        "tests/voice_perception/test_voice_message_not_command_without_intent_smoke.py",
    )

    for rel_path in (*required_files, *required_tests):
        assert (root / rel_path).exists(), rel_path

    read_model = build_voice_perception_status_read_model().to_read_model()
    assert read_model["phase_id"] == "PHASE_8"
    assert read_model["batch_id"] == "8.3"
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["action_execution_allowed"] is False
    assert read_model["microphone_runtime_started"] is False
    assert read_model["camera_runtime_started"] is False
    assert read_model["audio_playback_runtime_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["windows_voice_edge_parked"] is True
    assert read_model["push_to_talk_stt_live_parked"] is True
    assert read_model["junior_model_runtime_enabled"] is False
    assert read_model["local_inference_allowed"] is False

    acceptance_doc = (
        root
        / "docs/architecture/voice_perception/phase_8_voice_perception_acceptance_v1.md"
    ).read_text(encoding="utf-8").lower()
    for marker in (
        "phase 8 closed",
        "raw audio blocked by default",
        "text intent only",
        "owner voice gate required",
        "phase 9 junior model parked",
        "windows voice edge parked",
        "push-to-talk stt live parked",
        "no shell execution",
        "no pc control",
        "no second voice world",
    ):
        assert marker in acceptance_doc
