from __future__ import annotations

import json

from tools.monitor.runtime_input.network_containerization_web_preview import (
    build_network_containerization_web_preview_payload,
    render_network_containerization_web_preview_json,
)


def test_network_containerization_web_preview_payload_is_dashboard_safe() -> None:
    payload = build_network_containerization_web_preview_payload()

    assert payload["preview_id"] == "network_containerization_web_preview_v1"
    assert payload["rendering"]["dashboard_safe"] is True
    assert payload["rendering"]["read_only"] is True
    assert payload["rendering"]["deployment_action_available"] is False
    assert payload["read_model"]["deployment_allowed_now"] is False


def test_network_containerization_web_preview_renders_json() -> None:
    rendered = render_network_containerization_web_preview_json()
    payload = json.loads(rendered)

    assert payload["kind"] == "network_containerization_preview"
    assert payload["read_model"]["public_exposure_allowed"] is False
    assert payload["read_model"]["runtime_network_mutation_allowed"] is False
