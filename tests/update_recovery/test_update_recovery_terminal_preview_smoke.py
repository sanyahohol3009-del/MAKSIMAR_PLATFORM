from __future__ import annotations

import json
from pathlib import Path

from tools.monitor.runtime_input.update_recovery_terminal_preview import (
    build_update_recovery_preview_payload,
    render_update_recovery_terminal_preview,
)


def test_update_recovery_terminal_preview_is_dashboard_safe_json() -> None:
    payload = build_update_recovery_preview_payload(project_root=Path.cwd())

    assert payload["preview_id"] == "update_recovery_terminal_preview_v1"
    assert payload["dashboard_safe"] is True
    assert payload["runtime_apply_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["dashboard_execution_allowed"] is False
    assert payload["health"]["runtime_wrapper_only"] is True
    assert payload["health"]["existing_transport_preserved"] is True
    assert payload["health"]["existing_recovery_manager_preserved"] is True

    rendered = render_update_recovery_terminal_preview(project_root=Path.cwd())
    parsed = json.loads(rendered)
    assert parsed["preview_id"] == "update_recovery_terminal_preview_v1"
