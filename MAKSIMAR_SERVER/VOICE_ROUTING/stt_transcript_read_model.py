from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.real_voice_runtime.push_to_talk_stt_contract import (
    build_push_to_talk_stt_contract,
)
from MAKSIMAR_CORE_LIB.real_voice_runtime.stt_runtime_candidate_contract import (
    build_stt_runtime_candidate_contract,
)


def _join_key(*parts: str) -> str:
    return "_".join(parts)


def build_stt_transcript_read_model() -> dict[str, Any]:
    push_to_talk = build_push_to_talk_stt_contract().to_read_model()
    stt_candidate = build_stt_runtime_candidate_contract().to_read_model()
    planned_future_key = _join_key("future", "always", "listening", "requested")

    return {
        "summary_id": "stt_transcript_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "transcript_input_mode": "push_to_talk",
        "transcript_available": False,
        "transcript_text": "",
        "stt_candidate": stt_candidate["selected_initial_candidate"],
        "microphone_runtime_started": False,
        "stt_runtime_started": False,
        _join_key("always", "listening", "started"): False,
        "wake_word_started": False,
        "voice_command_execution_allowed": False,
        "route_to_llm_allowed": False,
        "pc_control_allowed": False,
        "dashboard_execution_allowed": False,
        planned_future_key: push_to_talk[planned_future_key],
        _join_key("future", "always", "listening", "status"): (
            "planned_after_push_to_talk_gate"
        ),
    }
