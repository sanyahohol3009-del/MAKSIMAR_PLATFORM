from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_binding_contract,
    build_project_artifact_phase_readiness,
    build_project_artifact_summary,
)


def test_phase_4_2_no_runtime_surface_smoke() -> None:
    bindings = build_project_artifact_binding_contract()
    summary = build_project_artifact_summary()
    readiness = build_project_artifact_phase_readiness()

    assert bindings.runtime_load_allowed_bindings == 0
    assert bindings.runtime_write_allowed_bindings == 0
    assert bindings.runtime_execution_allowed_bindings == 0

    assert summary["runtime_surface_allowed"] == 0
    assert readiness.no_runtime_load is True
    assert readiness.no_runtime_write is True
    assert readiness.no_runtime_execution is True
    assert readiness.no_runtime_surface is True
