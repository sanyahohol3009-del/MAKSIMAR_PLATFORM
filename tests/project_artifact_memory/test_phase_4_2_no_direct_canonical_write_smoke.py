from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_project_artifact_phase_readiness,
)


_FORBIDDEN_ROOTS = (
    "runtime_artifact_writer",
    "canonical_artifact_writer",
    "direct_canonical_artifact_writer",
    "artifact_runtime_executor",
    "model_runtime_loader",
)


def test_phase_4_2_no_direct_canonical_write_smoke() -> None:
    readiness = build_project_artifact_phase_readiness()

    assert readiness.no_forbidden_artifact_runtime_roots is True
    assert readiness.no_direct_canonical_write is True

    for root_name in _FORBIDDEN_ROOTS:
        assert not Path(root_name).exists()
