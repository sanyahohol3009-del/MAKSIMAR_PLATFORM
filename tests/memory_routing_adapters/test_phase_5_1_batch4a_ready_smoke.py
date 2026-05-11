from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_real_backend_security_boundary_preview,
)


def test_phase_5_1_batch4a_ready_smoke() -> None:
    preview = build_mempalace_real_backend_security_boundary_preview()

    assert preview["security_boundary_ready"] is True
    assert preview["filesystem_boundary_ready"] is True
    assert preview["network_boundary_ready"] is True
    assert preview["process_boundary_ready"] is True
    assert preview["manual_security_review_required"] is True
    assert preview["manual_security_review_completed"] is False
    assert preview["real_backend_candidate_detected"] is True
    assert preview["real_backend_enablement_allowed"] is False
    assert preview["real_backend_query_allowed"] is False
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
