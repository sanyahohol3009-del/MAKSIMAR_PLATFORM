from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.MEMORY_SYNC.mobile_capability_summary_builder import (
    build_mobile_ai_status_read_model,
)
from tools.mobile_ai_status_preview import build_mobile_ai_status_preview_payload


def test_phase_9_acceptance_artifacts_and_safety_markers_exist() -> None:
    root = Path(__file__).resolve().parents[2]

    required_files = (
        "shared_mobile_core/llm_engine/__init__.py",
        "shared_mobile_core/llm_engine/local_llm_runtime_contract.py",
        "shared_mobile_core/intent_parser/__init__.py",
        "shared_mobile_core/intent_parser/mobile_intent_parser_contract.py",
        "MAKSIMAR_CORE_LIB/app_safe_core/__init__.py",
        "MAKSIMAR_CORE_LIB/app_safe_core/app_safe_core_boundary_contract.py",
        "MAKSIMAR_CORE_LIB/app_safe_core/app_safe_core_export_manifest.py",
        "MAKSIMAR_CORE_LIB/mobile_bridge/mobile_core_mirror_contract.py",
        "MAKSIMAR_CORE_LIB/mobile_bridge/core_sync_protocol_contract.py",
        "MAKSIMAR_CORE_LIB/mobile_bridge/mirror_drift_detection_contract.py",
        "MAKSIMAR_CORE_LIB/mobile_bridge/junior_model_policy_contract.py",
        "MAKSIMAR_CORE_LIB/mobile_bridge/junior_model_eval_contract.py",
        "MAKSIMAR_SERVER/MEMORY_SYNC/mobile_capability_summary_builder.py",
        "MAKSIMAR_SERVER/MEMORY_SYNC/senior_to_junior_model_sync_contract.py",
        "MAKSIMAR_SERVER/MEMORY_SYNC/junior_feedback_ingest_contract.py",
        "MAKSIMAR_SERVER/MEMORY_SYNC/junior_model_sync_policy.py",
        "shared_mobile_core/mobile_sync_models/mobile_family_event_sync_contract.py",
        "ANDROID_SHELL/local_ai_runtime/android_local_ai_adapter_contract.py",
        "ANDROID_SHELL/local_ai_runtime/android_model_runtime_status.py",
        "ANDROID_SHELL/local_ai_runtime/android_training_sync_contract.py",
        "ANDROID_SHELL/local_ai_runtime/android_degraded_mode_contract.py",
        "IOS_SHELL/local_ai_runtime/ios_local_ai_adapter_contract.py",
        "IOS_SHELL/local_ai_runtime/ios_model_runtime_status.py",
        "IOS_SHELL/local_ai_runtime/ios_training_sync_contract.py",
        "IOS_SHELL/local_ai_runtime/ios_degraded_mode_contract.py",
        "tools/mobile_ai_status_preview.py",
        "CONTAINER_DEPLOYMENT/cubes/mobile_on_device_ai/container_contract.yaml",
        "docs/architecture/mobile_on_device_ai/phase_9_mobile_ai_acceptance_v1.md",
    )

    required_tests = (
        "tests/mobile_on_device_ai/test_local_llm_runtime_contract_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_intent_parser_contract_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_change_request_becomes_server_intent_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_junior_model_cannot_execute_core_actions_smoke.py",
        "tests/mobile_on_device_ai/test_app_safe_core_boundary_contract_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_core_mirror_contract_smoke.py",
        "tests/mobile_on_device_ai/test_core_sync_protocol_contract_smoke.py",
        "tests/mobile_on_device_ai/test_app_safe_core_mirror_read_only_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_mirror_cannot_execute_mutation_smoke.py",
        "tests/mobile_on_device_ai/test_mirror_drift_detection_contract_smoke.py",
        "tests/mobile_on_device_ai/test_junior_model_policy_contract_smoke.py",
        "tests/mobile_on_device_ai/test_junior_model_size_limit_default_smoke.py",
        "tests/mobile_on_device_ai/test_junior_model_eval_rationale_policy_smoke.py",
        "tests/mobile_on_device_ai/test_server_remains_canonical_core_smoke.py",
        "tests/mobile_on_device_ai/test_senior_to_junior_model_sync_contract_smoke.py",
        "tests/mobile_on_device_ai/test_junior_feedback_ingest_contract_smoke.py",
        "tests/mobile_on_device_ai/test_junior_model_sync_frequency_policy_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_ai_status_read_model_smoke.py",
        "tests/mobile_on_device_ai/test_android_local_ai_adapter_contract_smoke.py",
        "tests/mobile_on_device_ai/test_ios_local_ai_adapter_contract_smoke.py",
        "tests/mobile_on_device_ai/test_android_degraded_mode_contract_smoke.py",
        "tests/mobile_on_device_ai/test_ios_degraded_mode_contract_smoke.py",
        "tests/mobile_on_device_ai/test_mobile_ai_status_preview_smoke.py",
        "tests/container_readiness/test_mobile_on_device_ai_container_contract_smoke.py",
        "tests/mobile_on_device_ai/test_phase_9_acceptance_smoke.py",
    )

    for relative_path in required_files + required_tests:
        assert (root / relative_path).exists(), relative_path

    status = build_mobile_ai_status_read_model().to_read_model()
    preview = build_mobile_ai_status_preview_payload()
    data = preview["data"]

    assert preview["phase_id"] == "PHASE_9"
    assert status["server_jARVIS_is_senior"] is True
    assert status["mobile_junior_exists_as_app_safe_node"] is True
    assert status["app_safe_core_mirror_read_only"] is True
    assert status["junior_model_runtime_started"] is False
    assert status["model_download_allowed"] is False
    assert status["local_inference_started"] is False
    assert status["junior_can_execute_core_actions"] is False
    assert status["junior_can_write_canonical_memory"] is False
    assert status["junior_sync_authority"] is False
    assert status["feedback_is_proposal_only"] is True
    assert status["windows_voice_edge_parked"] is True
    assert status["push_to_talk_stt_live_parked"] is True

    assert data["network_sync_start_allowed"] is False
    assert data["deployment_allowed"] is False
    assert data["shell_execution_allowed"] is False
    assert data["canonical_write_allowed"] is False
    assert data["pc_control_allowed"] is False

    acceptance_doc = (
        root / "docs/architecture/mobile_on_device_ai/phase_9_mobile_ai_acceptance_v1.md"
    ).read_text(encoding="utf-8").lower()

    for marker in (
        "phase 9 closed",
        "server jarvis is senior",
        "mobile junior is subordinate",
        "app-safe core mirror is read-only",
        "model download allowed = false",
        "local inference started = false",
        "network sync start allowed = false",
        "shell execution allowed = false",
        "canonical write allowed = false",
        "pc control allowed = false",
        "phone control allowed = false",
        "windows voice edge parked",
        "push-to-talk stt live parked",
        "no second jarvis",
        "no second mobile ai world",
    ):
        assert marker in acceptance_doc
