from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_phase_preview,
    build_project_artifact_phase_readiness,
    build_project_artifact_preview,
    build_project_artifact_summary,
)


def test_phase_4_2_final_acceptance_smoke() -> None:
    summary = build_project_artifact_summary()
    preview = build_project_artifact_preview()
    readiness = build_project_artifact_phase_readiness()
    phase_preview = build_project_artifact_phase_preview()

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True
