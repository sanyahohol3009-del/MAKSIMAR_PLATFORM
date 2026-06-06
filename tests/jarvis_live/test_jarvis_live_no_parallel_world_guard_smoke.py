from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_roadmap_status_builder import (
    build_jarvis_live_roadmap_status,
)
from tools.project_readiness_control.jarvis_live_roadmap_expected_files import (
    FORBIDDEN_PARALLEL_WORLD_ROOTS,
    JARVIS_LIVE_REQUIRED_EXISTING_SURFACES,
    list_jarvis_live_roadmap_expected_paths,
)


def test_jarvis_live_expected_paths_are_exact_jl0_scope() -> None:
    expected_paths = list_jarvis_live_roadmap_expected_paths()

    assert expected_paths == (
        "docs/architecture/jarvis_live/jarvis_live_roadmap_v0_1.md",
        "docs/architecture/jarvis_live/jarvis_live_no_drift_rules_v0.md",
        "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_roadmap_status_builder.py",
        "tools/project_readiness_control/jarvis_live_roadmap_expected_files.py",
        "tests/jarvis_live/test_jarvis_live_roadmap_status_builder_smoke.py",
        "tests/jarvis_live/test_jarvis_live_no_parallel_world_guard_smoke.py",
    )


def test_jarvis_live_no_parallel_world_guard_is_clean() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["forbidden_parallel_world_roots"] == FORBIDDEN_PARALLEL_WORLD_ROOTS
    assert status["forbidden_parallel_world_roots_present"] == ()
    assert status["no_parallel_world_guard_ready"] is True


def test_jarvis_live_reuses_existing_canonical_surfaces() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["required_existing_surfaces"] == JARVIS_LIVE_REQUIRED_EXISTING_SURFACES
    assert status["missing_required_surfaces"] == ()
    assert "AI_SERVICES" in status["existing_required_surfaces"]
    assert "MAKSIMAR_CORE_LIB/workers_registry" in status["existing_required_surfaces"]
    assert "MAKSIMAR_CORE_LIB/execution_control" in status["existing_required_surfaces"]
    assert "MAKSIMAR_CORE_LIB/memory_engine" in status["existing_required_surfaces"]
    assert "MAKSIMAR_CORE_LIB/real_voice_runtime" in status[
        "existing_required_surfaces"
    ]
