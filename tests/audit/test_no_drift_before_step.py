from __future__ import annotations

import subprocess
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit import (
    build_project_surface_inventory,
    build_project_surface_summary,
)


def test_no_drift_before_step_project_surface_inventory_smoke() -> None:
    root = Path.cwd()
    inventory = build_project_surface_inventory(root)
    summary = build_project_surface_summary(root)

    assert len(inventory) > 0
    assert summary["total_surfaces"] > 0
    assert summary["critical_surfaces_present"] is True
    assert summary["missing_critical_surfaces"] == ()


def test_no_drift_before_step_forbidden_staged_surfaces_absent() -> None:
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"],
        text=True,
    ).strip()

    forbidden_prefixes = (
        "EXTERNAL_BACKENDS/mempalace/source/",
        "EXTERNAL_BACKENDS/mempalace/venv/",
        "EXTERNAL_BACKENDS/mempalace/sandbox_data/",
        "tests/runtime_core/",
    )

    for prefix in forbidden_prefixes:
        assert prefix not in staged
