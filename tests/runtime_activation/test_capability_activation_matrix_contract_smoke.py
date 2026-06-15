from __future__ import annotations

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


def test_runtime_activation_matrix_preview_is_json_safe() -> None:
    payload = build_runtime_activation_matrix_preview_payload()

    assert payload["schema_version"] == "1.0"
    assert payload["preview_kind"] == "read_only_capability_activation_matrix"
    assert payload["data"]["read_only"] is True
    assert payload["data"]["direct_execution_allowed"] is False
