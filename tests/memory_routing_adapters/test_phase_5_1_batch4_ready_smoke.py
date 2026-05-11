from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_runtime_sandbox_preview,
    build_mempalace_runtime_sandbox_summary,
)


def test_phase_5_1_batch4_ready_smoke() -> None:
    summary = build_mempalace_runtime_sandbox_summary()
    preview = build_mempalace_runtime_sandbox_preview()

    assert summary["sandbox_summary_ready"] is True
    assert preview["preview_ready"] is True
    assert summary["manual_security_review_required"] is True
    assert summary["hard_gate_passed"] is True
