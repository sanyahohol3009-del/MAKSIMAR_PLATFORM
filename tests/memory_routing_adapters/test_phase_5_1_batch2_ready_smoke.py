from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_adapter_surface,
    build_mempalace_guard_validation_report,
    build_mempalace_preview,
    build_mempalace_summary,
)


def test_phase_5_1_batch2_ready_smoke() -> None:
    guards = build_mempalace_guard_validation_report()
    surface = build_mempalace_adapter_surface()
    summary = build_mempalace_summary()
    preview = build_mempalace_preview()

    assert guards.guard_validation_ready is True
    assert surface.adapter_surface_ready is True
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["download_performed"] is False
    assert preview["real_backend_enabled"] is False
