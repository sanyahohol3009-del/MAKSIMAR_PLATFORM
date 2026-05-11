from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_runtime_sandbox_preview,
    build_mempalace_runtime_sandbox_summary,
)


def test_mempalace_runtime_sandbox_summary_preview_smoke() -> None:
    summary = build_mempalace_runtime_sandbox_summary()
    preview = build_mempalace_runtime_sandbox_preview()

    assert summary["sandbox_summary_ready"] is True
    assert summary["fake_backend_used"] is True
    assert summary["real_backend_candidate_detected"] is True
    assert summary["real_backend_enabled"] is False
    assert summary["real_backend_query_allowed"] is False
    assert summary["canonical_write_allowed"] is False
    assert summary["runtime_mutation_allowed"] is False

    assert preview["preview_ready"] is True
    assert preview["real_backend_enabled"] is False
    assert preview["real_backend_query_allowed"] is False
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
