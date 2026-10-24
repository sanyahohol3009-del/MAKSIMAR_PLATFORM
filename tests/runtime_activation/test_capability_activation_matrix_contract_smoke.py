from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.runtime_activation import (
    ACTIVATION_LEVELS,
    build_default_capability_activation_matrix,
)
from tools.runtime_activation_matrix_preview import (
    build_runtime_activation_matrix_preview_payload,
)


def test_capability_activation_matrix_is_read_only_and_explainable() -> None:
    matrix = build_default_capability_activation_matrix().to_read_model()

    assert matrix["read_only"] is True
    assert matrix["direct_execution_allowed"] is False
    assert matrix["canonical_write_allowed"] is False
    assert matrix["pc_control_allowed"] is False
    assert matrix["phone_control_allowed"] is False
    assert matrix["deployment_allowed"] is False

    entries = matrix["entries"]
    assert entries

    by_id = {entry["capability_id"]: entry for entry in entries}
    for expected_id in (
        "voice_perception",
        "mobile_on_device_ai",
        "android_junior_model",
        "ios_junior_model",
        "runtime_history_store",
        "ollama_local_engine",
        "pc_control_candidates",
        "windows_voice_edge_runtime",
        "push_to_talk_stt_live",
        "screen_observer_readonly",
        "retrieval_readonly_tools",
        "mgrep_readonly",
        "sqlite_vec_readonly",
        "qdrant_readonly_status",
        "approval_gates",
        "network_sync_gates",
    ):
        assert expected_id in by_id

    for entry in entries:
        assert entry["capability_present"] is True
        assert entry["contract_valid"] is True
        assert entry["activation_level"] in ACTIVATION_LEVELS
        assert entry["blocked_reason"]
        assert entry["next_required_action"]
        assert entry["evidence_refs"]

    assert by_id["android_junior_model"]["model_present"] is False
    assert by_id["android_junior_model"]["runtime_started"] is False
    assert by_id["ios_junior_model"]["model_present"] is False
    assert by_id["ios_junior_model"]["runtime_started"] is False
    assert by_id["pc_control_candidates"]["activation_level"] == "LEVEL_0_CONTRACT_ONLY"
    assert by_id["windows_voice_edge_runtime"]["runtime_started"] is False
    assert by_id["push_to_talk_stt_live"]["runtime_started"] is False
    assert by_id["push_to_talk_stt_live"]["activation_level"] == "LEVEL_1_VISIBLE_READ_ONLY"
    assert by_id["network_sync_gates"]["activation_level"] == "LEVEL_0_CONTRACT_ONLY"
    assert by_id["approval_gates"]["policy_allowed"] is False


def test_runtime_activation_matrix_preview_is_json_safe() -> None:
    payload = build_runtime_activation_matrix_preview_payload()

    assert payload["schema_version"] == "1.0"
    assert payload["preview_kind"] == "read_only_capability_activation_matrix"
    assert payload["data"]["read_only"] is True
    assert payload["data"]["direct_execution_allowed"] is False

def test_activation_matrix_question_contract_is_typed_read_only_data() -> None:
    payload = build_runtime_activation_matrix_preview_payload()
    assert payload["preview_kind"] == "read_only_capability_activation_matrix"
    assert payload["data"]["read_only"] is True
    assert payload["data"]["direct_execution_allowed"] is False


def test_activation_matrix_contract_does_not_parse_user_text() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(encoding="utf-8")
    assert "_build_read_only_tool_plan" not in source
    assert "jarvis_live_request_planner" not in source


def test_activation_matrix_answer_exposes_voice_and_mobile_juniors() -> None:
    from tools.jarvis_live_runtime.jarvis_live_brain_loop import _format_activation_matrix_answer

    answer = _format_activation_matrix_answer()

    assert "windows_voice_edge_runtime" in answer
    assert "push_to_talk_stt_live" in answer
    assert "android_junior_model" in answer
    assert "ios_junior_model" in answer
    assert "JARVIS остаётся senior/canonical authority" in answer
    assert "capability_scoped_policy=active" in answer
    assert "protected_execution_requires_approval=true" in answer
    assert "runtime_started=false" in answer
