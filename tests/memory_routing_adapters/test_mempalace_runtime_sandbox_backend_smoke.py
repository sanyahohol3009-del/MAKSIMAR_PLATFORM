from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_fake_backend_query_result,
    build_mempalace_real_backend_candidate_state,
)


def test_mempalace_runtime_sandbox_backend_smoke() -> None:
    fake_query = build_mempalace_fake_backend_query_result()
    real_candidate = build_mempalace_real_backend_candidate_state()

    assert fake_query.result_ready is True
    assert fake_query.fake_backend_used is True
    assert fake_query.real_backend_enabled is False
    assert fake_query.canonical_write_allowed is False
    assert fake_query.runtime_mutation_allowed is False

    assert real_candidate.candidate_state_ready is True
    assert real_candidate.real_backend_candidate_detected is True
    assert real_candidate.real_backend_enabled is False
    assert real_candidate.real_backend_query_allowed is False
    assert real_candidate.canonical_write_allowed is False
    assert real_candidate.runtime_mutation_allowed is False
