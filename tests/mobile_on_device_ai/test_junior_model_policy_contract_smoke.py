from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.junior_model_policy_contract import (
    build_junior_model_policy_contract,
)


def test_junior_model_policy_contract_keeps_runtime_parked() -> None:
    read_model = build_junior_model_policy_contract().to_read_model()

    assert read_model["junior_model_role"] == "mobile_junior"
    assert read_model["senior_model_role"] == "server_jARVIS_senior"
    assert read_model["junior_model_allowed"] is True
    assert read_model["app_safe_only"] is True
    assert read_model["text_intent_only"] is True
    assert read_model["local_inference_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["canonical_truth_allowed"] is False
    assert read_model["core_action_execution_allowed"] is False
    assert read_model["server_remains_canonical_authority"] is True
