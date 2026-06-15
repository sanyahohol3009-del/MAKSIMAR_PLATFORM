from __future__ import annotations

from pathlib import Path

from tools.mobile_ai_status_preview import build_mobile_ai_status_preview_payload


def test_mobile_ai_status_preview_payload_is_read_only_phase_9_status() -> None:
    payload = build_mobile_ai_status_preview_payload()
    data = payload["data"]

    assert payload["schema_version"] == "1.0"
    assert payload["phase_id"] == "PHASE_9"
    assert data["phase_id"] == "PHASE_9"
    assert data["server_jARVIS_is_senior"] is True
    assert data["mobile_junior_exists_as_app_safe_node"] is True
    assert data["app_safe_core_mirror_read_only"] is True
    assert data["junior_model_runtime_started"] is False
    assert data["model_download_allowed"] is False
    assert data["local_inference_started"] is False
    assert data["junior_can_execute_core_actions"] is False
    assert data["junior_can_write_canonical_memory"] is False
    assert data["junior_sync_authority"] is False
    assert data["feedback_is_proposal_only"] is True
    assert data["windows_voice_edge_parked"] is True
    assert data["push_to_talk_stt_live_parked"] is True
    assert data["network_sync_start_allowed"] is False
    assert data["deployment_allowed"] is False
    assert data["shell_execution_allowed"] is False
    assert data["canonical_write_allowed"] is False
    assert data["pc_control_allowed"] is False


def test_mobile_ai_status_preview_does_not_import_runtime_or_network_modules() -> None:
    source = Path("tools/mobile_ai_status_preview.py").read_text(encoding="utf-8")

    for blocked_import in (
        "import subprocess",
        "import requests",
        "import httpx",
        "import aiohttp",
        "import socket",
        "import docker",
        "from subprocess",
        "from requests",
        "from httpx",
        "from aiohttp",
        "from socket",
        "from docker",
    ):
        assert blocked_import not in source
