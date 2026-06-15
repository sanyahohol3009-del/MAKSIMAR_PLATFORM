from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC.junior_model_sync_policy import (
    build_junior_model_sync_policy,
)


def test_junior_model_sync_frequency_policy_is_controlled() -> None:
    read_model = build_junior_model_sync_policy().to_read_model()

    assert read_model["sync_frequency_policy_enabled"] is True
    assert read_model["default_sync_mode"] == "controlled"
    assert read_model["continuous_sync_allowed"] is False
    assert read_model["background_sync_allowed"] is False
    assert read_model["offline_queue_allowed"] is True
    assert read_model["offline_queue_canonical"] is False
    assert read_model["sync_requires_policy"] is True
    assert read_model["sync_requires_server_presence_or_floating_master"] is True
    assert read_model["junior_sync_authority"] is False
    assert read_model["conflict_resolution_on_server_only"] is True
    assert read_model["server_remains_canonical_authority"] is True
    assert read_model["model_download_allowed"] is False
    assert read_model["local_inference_started"] is False
