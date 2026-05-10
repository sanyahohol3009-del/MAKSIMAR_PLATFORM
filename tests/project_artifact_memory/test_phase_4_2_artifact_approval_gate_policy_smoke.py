from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_phase_preview,
    build_project_artifact_phase_readiness,
)


def test_phase_4_2_artifact_approval_gate_policy_smoke() -> None:
    readiness = build_project_artifact_phase_readiness()
    preview = build_project_artifact_phase_preview()

    assert readiness.artifact_write_approval_gate_required is True
    assert readiness.sandbox_staging_only_future_write_path is True
    assert readiness.no_direct_canonical_write is True

    assert preview["artifact_write_approval_gate_required"] is True
    assert preview["sandbox_staging_only_future_write_path"] is True
    assert preview["no_direct_canonical_write"] is True
