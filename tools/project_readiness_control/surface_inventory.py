"""Read-only project surface inventory sub-runner.

This module reuses the existing project_surface_audit surface. It does not
create a second inventory engine and does not mutate the repository.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Mapping

from MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit import (
    build_project_surface_inventory,
    build_project_surface_summary,
)


@dataclass(frozen=True, slots=True)
class SurfaceInventoryRunResult:
    project_root: str
    total_surfaces: int
    tracked_surfaces: int
    untracked_surfaces: int
    critical_surfaces_present: bool
    source_surface: str = "MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit"
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.project_root:
            raise ValueError("project_root must not be empty")
        if self.total_surfaces < 0:
            raise ValueError("total_surfaces must not be negative")
        if self.tracked_surfaces < 0:
            raise ValueError("tracked_surfaces must not be negative")
        if self.untracked_surfaces < 0:
            raise ValueError("untracked_surfaces must not be negative")
        if self.tracked_surfaces + self.untracked_surfaces > self.total_surfaces:
            raise ValueError("tracked + untracked must not exceed total_surfaces")
        if not self.source_surface:
            raise ValueError("source_surface must not be empty")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")


def _mapping_from_object(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "__dict__"):
        return vars(value)
    return {}


def _count_inventory_entries(inventory: tuple[Any, ...]) -> tuple[int, int]:
    tracked = 0
    untracked = 0

    for entry in inventory:
        mapped = _mapping_from_object(entry)
        status = str(mapped.get("git_status") or mapped.get("status") or "").lower()
        is_tracked = mapped.get("tracked")

        if is_tracked is True or status == "tracked":
            tracked += 1
        elif is_tracked is False or status == "untracked":
            untracked += 1

    return tracked, untracked


def run_surface_inventory(project_root: str | Path = ".") -> SurfaceInventoryRunResult:
    root = Path(project_root)
    inventory = tuple(build_project_surface_inventory(root))
    summary = build_project_surface_summary(root)

    if not isinstance(summary, Mapping):
        raise TypeError("build_project_surface_summary must return a mapping")

    counted_tracked, counted_untracked = _count_inventory_entries(inventory)

    total_surfaces = int(summary.get("total_surfaces", len(inventory)))
    tracked_surfaces = int(summary.get("tracked_surfaces", counted_tracked))
    untracked_surfaces = int(summary.get("untracked_surfaces", counted_untracked))
    critical_surfaces_present = bool(summary.get("critical_surfaces_present", True))

    return SurfaceInventoryRunResult(
        project_root=str(root),
        total_surfaces=total_surfaces,
        tracked_surfaces=tracked_surfaces,
        untracked_surfaces=untracked_surfaces,
        critical_surfaces_present=critical_surfaces_present,
    )
