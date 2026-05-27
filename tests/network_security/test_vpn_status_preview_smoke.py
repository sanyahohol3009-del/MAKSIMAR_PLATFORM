from __future__ import annotations

import json
import subprocess
import sys

from tools.vpn_status_preview import build_vpn_status_preview_payload, main


def test_vpn_status_preview_payload_smoke() -> None:
    payload = build_vpn_status_preview_payload()

    assert payload["preview_id"] == "phase_2_vpn_status_preview"
    assert payload["preview_mode"] == "read_only"
    assert payload["read_only"] is True
    assert payload["action_buttons_enabled"] is False
    assert payload["direct_execution_allowed"] is False
    assert payload["ports_opened"] is False
    assert payload["containers_started"] is False
    assert payload["active_deployment_created"] is False
    assert payload["external_network_access_enabled"] is False
    assert "control-plane handoff" in payload["operator_message"]


def test_vpn_status_preview_main_outputs_json_smoke(capsys) -> None:
    main()
    captured = capsys.readouterr()

    payload = json.loads(captured.out)
    assert payload["preview_id"] == "phase_2_vpn_status_preview"
    assert payload["preview_mode"] == "read_only"
    assert payload["action_buttons_enabled"] is False


def test_vpn_status_preview_script_executes_directly_smoke() -> None:
    result = subprocess.run(
        [sys.executable, "tools/vpn_status_preview.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["preview_id"] == "phase_2_vpn_status_preview"
    assert payload["preview_mode"] == "read_only"
    assert payload["read_only"] is True
    assert payload["action_buttons_enabled"] is False
    assert payload["direct_execution_allowed"] is False
