from __future__ import annotations

from IOS_SHELL.local_ai_runtime.ios_local_ai_adapter_contract import (
    build_ios_local_ai_adapter_contract,
)


def test_ios_local_ai_adapter_contract_is_capability_only() -> None:
    read_model = build_ios_local_ai_adapter_contract().to_read_model()

    assert read_model["platform"] == "ios"
    assert read_model["local_ai_adapter_contract"] is True
    assert read_model["junior_model_role"] == "mobile_junior"
    assert read_model["senior_model_role"] == "server_jARVIS_senior"
    assert read_model["app_safe_only"] is True
    assert read_model["text_intent_only"] is True
    assert read_model["local_model_runtime_supported"] is True
    assert read_model["local_model_runtime_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["local_inference_started"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["canonical_memory_write_allowed"] is False
    assert read_model["core_action_execution_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["phone_control_allowed"] is False
    assert read_model["deployment_allowed"] is False
    assert read_model["proposal_only"] is True
