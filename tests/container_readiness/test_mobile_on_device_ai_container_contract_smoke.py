from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CONTAINER_CONTRACT = Path(
    "CONTAINER_DEPLOYMENT/cubes/mobile_on_device_ai/container_contract.yaml"
)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_mobile_on_device_ai_container_contract_is_preview_only() -> None:
    assert CONTAINER_CONTRACT.exists()

    contract = _load_yaml(CONTAINER_CONTRACT)

    assert contract["cube_id"] == "mobile_on_device_ai"
    assert contract["phase"] == "PHASE_9"
    assert contract["read_only"] is True
    assert contract["preview_only"] is True
    assert contract["runtime_start_allowed"] is False
    assert contract["model_download_allowed"] is False
    assert contract["local_inference_start_allowed"] is False
    assert contract["network_sync_start_allowed"] is False
    assert contract["shell_execution_allowed"] is False
    assert contract["canonical_write_allowed"] is False
    assert contract["canonical_memory_write_allowed"] is False
    assert contract["core_action_execution_allowed"] is False
    assert contract["pc_control_allowed"] is False
    assert contract["direct_mobile_control_allowed"] is False
    assert contract["phone_control_allowed"] is False
    assert contract["deployment_allowed"] is False
    assert contract["proposal_only"] is True
    assert contract["server_jARVIS_is_senior"] is True
    assert contract["mobile_junior_is_subordinate"] is True
    assert contract["app_safe_only"] is True
    assert contract["text_intent_only"] is True
    assert contract["windows_voice_edge_parked"] is True
    assert contract["push_to_talk_stt_live_parked"] is True
    assert (
        contract["read_model_source"]
        == "MAKSIMAR_SERVER/MEMORY_SYNC/mobile_capability_summary_builder.py"
    )
    assert contract["preview_tool"] == "tools/mobile_ai_status_preview.py"
