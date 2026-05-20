from __future__ import annotations

from tools.monitor.runtime_input.network_containerization_terminal_preview import (
    build_network_containerization_preview_read_model,
    render_network_containerization_terminal_preview,
)


def test_network_containerization_terminal_preview_is_read_only_and_safe() -> None:
    preview = build_network_containerization_preview_read_model()

    assert preview.read_model_id == "network_containerization_preview_read_model_v1"
    assert preview.dashboard_safe is True
    assert preview.read_only is True
    assert preview.deployment_allowed_now is False
    assert preview.public_exposure_allowed is False
    assert preview.runtime_network_mutation_allowed is False
    assert preview.blocked_edges


def test_network_containerization_terminal_preview_renders_blocked_edges() -> None:
    rendered = render_network_containerization_terminal_preview()

    assert "NETWORK_CONTAINERIZATION PREVIEW" in rendered
    assert "blocked_edges:" in rendered
    assert "deployment_allowed_now: False" in rendered
    assert "public_exposure_allowed: False" in rendered
