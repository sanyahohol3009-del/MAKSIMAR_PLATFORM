from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_phase_preview,
    build_project_artifact_preview,
)


def test_phase_4_2_visible_preview_smoke() -> None:
    preview = build_project_artifact_preview()
    phase_preview = build_project_artifact_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["artifact_bindings"] == 8
    assert preview["runtime_surface_allowed"] == 0

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["artifact_bindings"] == 8
    assert phase_preview["no_runtime_surface"] is True
    assert phase_preview["no_direct_canonical_write"] is True
