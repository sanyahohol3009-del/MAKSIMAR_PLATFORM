from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_real_backend_security_boundary,
)


def test_mempalace_real_backend_security_boundary_smoke() -> None:
    boundary = build_mempalace_real_backend_security_boundary()

    assert boundary.security_boundary_ready is True
    assert boundary.filesystem.filesystem_boundary_ready is True
    assert boundary.network.network_boundary_ready is True
    assert boundary.process.process_boundary_ready is True
    assert boundary.manual_security_review_required is True
    assert boundary.manual_security_review_completed is False
    assert boundary.real_backend_candidate_detected is True
    assert boundary.real_backend_enablement_allowed is False
    assert boundary.real_backend_query_allowed is False
    assert boundary.canonical_write_allowed is False
    assert boundary.runtime_mutation_allowed is False
