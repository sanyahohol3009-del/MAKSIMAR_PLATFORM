from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_runtime_sandbox_preview,
)


def test_phase_5_1_batch4_no_real_backend_enablement_smoke() -> None:
    preview = build_mempalace_runtime_sandbox_preview()

    assert preview["real_backend_candidate_detected"] is True
    assert preview["real_backend_enabled"] is False
    assert preview["real_backend_query_allowed"] is False
    assert preview["manual_security_review_required"] is True
    assert preview["canonical_write_allowed"] is False
    assert preview["auto_promotion_allowed"] is False
    assert preview["auto_conflict_resolution_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
