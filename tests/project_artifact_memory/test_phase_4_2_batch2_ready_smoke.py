from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_binding_contract,
    build_project_artifact_preview,
    build_project_artifact_summary,
)


def test_phase_4_2_batch2_ready_smoke() -> None:
    bindings = build_project_artifact_binding_contract()
    summary = build_project_artifact_summary()
    preview = build_project_artifact_preview()

    assert bindings.ready_bindings == bindings.total_bindings
    assert bindings.read_only_bindings == bindings.total_bindings
    assert bindings.runtime_load_allowed_bindings == 0
    assert bindings.runtime_write_allowed_bindings == 0
    assert bindings.runtime_execution_allowed_bindings == 0
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
