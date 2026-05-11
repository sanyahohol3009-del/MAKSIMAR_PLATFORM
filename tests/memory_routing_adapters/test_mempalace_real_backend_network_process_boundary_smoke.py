from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_network_boundary,
    build_mempalace_process_boundary,
)


def test_mempalace_real_backend_network_process_boundary_smoke() -> None:
    network = build_mempalace_network_boundary()
    process = build_mempalace_process_boundary()

    assert network.network_boundary_ready is True
    assert network.network_default_policy == "disabled_until_explicit_review"
    assert network.outbound_network_allowed is False
    assert network.external_download_allowed is False
    assert network.remote_model_api_allowed is False
    assert network.local_loopback_allowed is False
    assert network.network_review_required is True

    assert process.process_boundary_ready is True
    assert process.separate_venv_required is True
    assert process.isolated_workdir_required is True
    assert process.env_scrub_required is True
    assert process.project_env_inheritance_allowed is False
    assert process.secrets_access_allowed is False
    assert process.shell_execution_allowed is False
    assert process.subprocess_execution_allowed is False
