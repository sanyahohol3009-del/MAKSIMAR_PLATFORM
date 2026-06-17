from __future__ import annotations

import pytest

from tools.jarvis_live_runtime.stt_engine_policy import build_default_stt_engine_policy
from tools.jarvis_live_runtime.tts_voice_profile_policy import build_default_tts_voice_profile_policy
from tools.jarvis_live_runtime.voice_edge_v2_policy import build_default_voice_edge_v2_policy
from tools.jarvis_live_runtime.voice_personality_policy_contract import (
    build_default_voice_personality_policy,
)
from tools.jarvis_live_runtime.voice_response_cleaner import (
    contains_forbidden_generic_tail,
    guarded_voice_response,
)
from tools.jarvis_live_runtime.voice_response_mode_policy import classify_voice_response_mode
from tools.jarvis_live_runtime.wake_vad_echo_guard_policy import (
    build_default_wake_vad_echo_guard_policy,
)


def test_voice_edge_v2_routes_only_to_control_plane() -> None:
    policy = build_default_voice_edge_v2_policy()

    assert "127.0.0.1:8765" in policy.control_plane_stream_url
    assert "11434" not in policy.control_plane_stream_url
    assert policy.direct_ollama_allowed is False
    assert policy.pc_control_allowed is False
    assert policy.direct_execution_allowed is False
    assert policy.public_network_allowed is False
    assert policy.tunnel_allowed is False


def test_voice_personality_blocks_generic_tails() -> None:
    policy = build_default_voice_personality_policy()

    assert policy.assistant_identity == "JARVIS"
    assert policy.pc_control_allowed is False
    assert policy.direct_execution_allowed is False
    assert "Чем могу помочь?" in policy.forbidden_generic_tails

    assert contains_forbidden_generic_tail("Принял. Чем могу помочь?") is True
    assert guarded_voice_response("Принял. Чем могу помочь?") == "Принял."


def test_response_mode_keeps_actions_approval_gated() -> None:
    mode = classify_voice_response_mode("открой браузер")

    assert mode.response_mode == "approval_required"
    assert mode.approval_required is True
    assert mode.pc_control_allowed is False
    assert mode.direct_execution_allowed is False


def test_stt_policy_rejects_vosk_as_primary() -> None:
    policy = build_default_stt_engine_policy()
    read_model = policy.to_read_model()

    primary = [c for c in read_model["candidates"] if c["role"] == "primary"]
    legacy = [c for c in read_model["candidates"] if c["engine_kind"] == "vosk"]

    assert primary[0]["engine_kind"] == "faster_whisper"
    assert primary[0]["model_id"] == "large-v3-turbo"
    assert legacy[0]["legacy_only"] is True
    assert legacy[0]["primary_allowed"] is False
    assert policy.raw_audio_to_core_allowed is False


def test_tts_policy_rejects_piper_denis_as_primary() -> None:
    policy = build_default_tts_voice_profile_policy()
    profiles = policy.to_read_model()["profiles"]

    piper = [p for p in profiles if p["voice_id"] == "ru_RU-denis-medium"][0]
    assert piper["rejected_as_primary"] is True
    assert piper["primary_allowed"] is False


def test_wake_vad_echo_guard_keeps_final_always_listening() -> None:
    policy = build_default_wake_vad_echo_guard_policy()

    assert policy.always_listening_required_for_final is True
    assert policy.push_to_talk_allowed_as_final is False
    assert policy.wake_word_required is True
    assert policy.vad_required is True
    assert policy.echo_suppression_required is True
    assert policy.raw_audio_storage_allowed is False
    assert policy.raw_audio_to_core_allowed is False


def test_invalid_direct_ollama_policy_fails() -> None:
    from tools.jarvis_live_runtime.voice_edge_v2_policy import VoiceEdgeV2Policy

    with pytest.raises(ValueError):
        VoiceEdgeV2Policy(
            policy_id="bad",
            control_plane_stream_url="http://127.0.0.1:11434/api/generate",
            control_plane_health_url="http://127.0.0.1:8765/jarvis-live/health",
            direct_ollama_allowed=True,
            pc_control_allowed=False,
            direct_execution_allowed=False,
            public_network_allowed=False,
            tunnel_allowed=False,
            final_mode_requires_always_listening=True,
        )
