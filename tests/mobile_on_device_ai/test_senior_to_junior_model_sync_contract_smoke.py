from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC.senior_to_junior_model_sync_contract import (
    build_senior_to_junior_model_sync_contract,
)


def test_senior_to_junior_model_sync_contract_is_read_only() -> None:
    read_model = build_senior_to_junior_model_sync_contract().to_read_model()

    assert read_model["sync_contract_enabled"] is True
    assert read_model["sync_direction"] == "server_senior_to_mobile_junior"
    assert read_model["server_jARVIS_is_senior"] is True
    assert read_model["mobile_junior_is_subordinate"] is True
    assert read_model["sync_payload_is_app_safe"] is True
    assert read_model["sync_payload_is_read_only"] is True
    assert read_model["sync_payload_is_intent_context_only"] is True
    assert read_model["canonical_core_export_allowed"] is False
    assert read_model["canonical_memory_write_allowed"] is False
    assert read_model["junior_canonical_write_allowed"] is False
    assert read_model["junior_core_action_execution_allowed"] is False
    assert read_model["junior_shell_execution_allowed"] is False
    assert read_model["junior_pc_control_allowed"] is False
    assert read_model["junior_direct_phone_control_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["local_inference_started"] is False
    assert read_model["windows_voice_edge_parked"] is True
    assert read_model["push_to_talk_stt_live_parked"] is True
    assert read_model["proposal_only"] is True
