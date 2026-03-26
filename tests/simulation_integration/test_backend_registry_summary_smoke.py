from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration import (
    build_simulation_backend_summary,
)


def test_simulation_backend_summary_builds() -> None:
    """Simulation backend summary should build successfully."""
    summary = build_simulation_backend_summary()

    assert summary.total_backends >= 1
    assert len(summary.records) == summary.total_backends


def test_simulation_backend_summary_contains_pybullet() -> None:
    """Simulation backend summary should contain pybullet backend."""
    summary = build_simulation_backend_summary()

    assert any(
        record.backend_id == "simulation_backend_pybullet"
        for record in summary.records
    )
