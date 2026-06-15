from __future__ import annotations

from shared_mobile_core.llm_engine.local_llm_runtime_contract import (
    build_local_llm_runtime_contract,
)


def test_local_llm_runtime_contract_stays_capability_only() -> None:
    read_model = build_local_llm_runtime_contract().to_read_model()

    assert read_model["junior_model_role"] == "mobile_junior"
    assert read_model["senior_model_role"] == "server_jARVIS_senior"
    assert read_model["local_llm_runtime_allowed"] is True
    assert read_model["local_llm_runtime_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["canonical_truth_allowed"] is False
    assert read_model["canonical_memory_write_allowed"] is False
    assert read_model["core_action_execution_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["proposal_only"] is True
    assert read_model["app_safe_only"] is True
