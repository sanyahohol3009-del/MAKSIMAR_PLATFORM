from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC.mobile_capability_summary_builder import (
    build_mobile_ai_status_read_model,
)


def test_mobile_ai_status_read_model_keeps_server_senior_authority() -> None:
    read_model = build_mobile_ai_status_read_model().to_read_model()

    assert read_model["server_jARVIS_is_senior"] is True
    assert read_model["mobile_junior_exists_as_app_safe_node"] is True
    assert read_model["app_safe_core_mirror_read_only"] is True
    assert read_model["junior_model_runtime_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["local_inference_started"] is False
    assert read_model["junior_can_execute_core_actions"] is False
    assert read_model["junior_can_write_canonical_memory"] is False
    assert read_model["junior_sync_authority"] is False
    assert read_model["feedback_is_proposal_only"] is True
    assert read_model["windows_voice_edge_parked"] is True
    assert read_model["push_to_talk_stt_live_parked"] is True
