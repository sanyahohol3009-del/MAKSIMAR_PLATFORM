import json
import subprocess
import sys

from tools.workflow_status_preview import build_workflow_status_preview_payload


def test_workflow_status_preview_payload_is_read_only() -> None:
    payload = build_workflow_status_preview_payload()

    assert payload["preview_read_only"] is True
    assert payload["dashboard_read_only"] is True
    assert payload["runtime_execution_allowed"] is False
    assert payload["direct_core_write_allowed"] is False
    assert payload["direct_server_canonical_write_allowed"] is False
    assert payload["network_socket_tunnel_allowed"] is False
    assert payload["workflow_status"]["dashboard_execution_allowed"] is False
    assert payload["dashboard_projection"]["action_controls_enabled"] is False
    assert payload["dashboard_projection"]["execution_controls_enabled"] is False
    assert payload["dashboard_projection"]["mutation_controls_enabled"] is False


def test_workflow_status_preview_cli_outputs_json() -> None:
    result = subprocess.run(
        [sys.executable, "tools/workflow_status_preview.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["preview_id"] == "phase6.workflow.status.preview.v1"
    assert payload["workflow_status"]["bridge_id"] == "phase6.workflow.status.bridge.v1"
    assert payload["workflow_status"]["network_disabled_by_default"] is True
