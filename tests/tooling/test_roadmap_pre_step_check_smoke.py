from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit import (
    build_project_surface_inventory,
    build_project_surface_summary,
)


def test_project_surface_audit_inventory_smoke() -> None:
    inventory = build_project_surface_inventory(Path.cwd())
    summary = build_project_surface_summary(Path.cwd())

    assert len(inventory) > 0
    assert summary["total_surfaces"] > 0
    assert summary["critical_surfaces_present"] is True


def test_roadmap_pre_step_check_tool_smoke() -> None:
    tool = Path("tools/roadmap_pre_step_check.py")

    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool), "--inventory-only"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "Total surfaces:" in completed.stdout
