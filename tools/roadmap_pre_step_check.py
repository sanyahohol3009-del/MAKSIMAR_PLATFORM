from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit import (
    build_project_surface_inventory,
    build_project_surface_summary,
)


def run(command: list[str], label: str) -> None:
    print(f"===== {label} =====")
    completed = subprocess.run(command, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="MAKSIMAR roadmap pre-step check.")
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()

    if not args.inventory_only:
        run(
            [sys.executable, "-m", "pytest", "tests/audit/test_no_drift_before_step.py", "-q", "--tb=short"],
            "ROADMAP PRE-STEP NO DRIFT TEST",
        )

    inventory = build_project_surface_inventory(root)
    summary = build_project_surface_summary(root)

    print("===== ROADMAP PRE-STEP PROJECT SURFACE INVENTORY =====")
    print(f"Total surfaces: {len(inventory)}")
    print(f"Tracked surfaces: {summary['tracked_surfaces']}")
    print(f"Untracked surfaces: {summary['untracked_surfaces']}")
    print(f"Critical surfaces present: {summary['critical_surfaces_present']}")

    if summary["critical_surfaces_present"] is not True:
        raise SystemExit("ERROR: missing critical project surfaces")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
