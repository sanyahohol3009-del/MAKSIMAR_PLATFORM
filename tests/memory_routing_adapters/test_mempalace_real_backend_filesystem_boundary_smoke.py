from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_filesystem_boundary,
)


def test_mempalace_real_backend_filesystem_boundary_smoke() -> None:
    boundary = build_mempalace_filesystem_boundary()

    assert boundary.filesystem_boundary_ready is True
    assert boundary.allowed_write_roots == ("EXTERNAL_BACKENDS/mempalace/sandbox_data",)
    assert "CORE_ROOT" in boundary.denied_roots
    assert "RUNTIME" in boundary.denied_roots
    assert "SUPERVISOR" in boundary.denied_roots
    assert boundary.sandbox_data_only is True
    assert boundary.canonical_memory_access is False
    assert boundary.canonical_artifact_access is False
    assert boundary.runtime_state_access is False
    assert boundary.destructive_operations_allowed is False
