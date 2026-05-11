from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


IGNORED_ROOTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "__pycache__",
}

IGNORED_FILENAMES = {
    ".pymon",
    ".coverage",
}

IGNORED_EXTERNAL_SUBTREES = (
    "EXTERNAL_BACKENDS/mempalace/source",
    "EXTERNAL_BACKENDS/mempalace/venv",
    "EXTERNAL_BACKENDS/mempalace/sandbox_data",
)

CRITICAL_SURFACES = (
    "BOOT",
    "CORE_ROOT",
    "MAKSIMAR_CORE_LIB",
    "MAKSIMAR_SERVER",
    "SUPERVISOR",
    "tests",
    "tools",
)


@dataclass(frozen=True, slots=True)
class ProjectSurfaceEntry:
    path: str
    surface_kind: str
    tracked_by_git: bool


def _git_ls_files(root: Path) -> set[str]:
    try:
        output = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).strip()
    except Exception:
        return set()

    return set(line.strip() for line in output.splitlines() if line.strip())


def _is_ignored(path: str) -> bool:
    if not path:
        return True

    first = path.split("/", 1)[0]
    if first in IGNORED_ROOTS:
        return True

    if path in IGNORED_FILENAMES:
        return True

    return any(path == ignored or path.startswith(f"{ignored}/") for ignored in IGNORED_EXTERNAL_SUBTREES)


def build_project_surface_inventory(project_root: Path) -> Tuple[ProjectSurfaceEntry, ...]:
    project_root = project_root.resolve()
    tracked = _git_ls_files(project_root)

    entries: list[ProjectSurfaceEntry] = []

    for child in sorted(project_root.iterdir(), key=lambda item: item.name):
        rel = child.relative_to(project_root).as_posix()

        if _is_ignored(rel):
            continue

        if child.is_dir():
            surface_kind = "directory"
            tracked_by_git = any(item == rel or item.startswith(f"{rel}/") for item in tracked)
        elif child.is_file():
            surface_kind = "file"
            tracked_by_git = rel in tracked
        else:
            surface_kind = "other"
            tracked_by_git = False

        entries.append(
            ProjectSurfaceEntry(
                path=rel,
                surface_kind=surface_kind,
                tracked_by_git=tracked_by_git,
            )
        )

    return tuple(entries)


def build_project_surface_summary(project_root: Path) -> dict[str, object]:
    inventory = build_project_surface_inventory(project_root)
    paths = tuple(entry.path for entry in inventory)

    missing_critical = tuple(surface for surface in CRITICAL_SURFACES if surface not in paths)

    return {
        "total_surfaces": len(inventory),
        "tracked_surfaces": sum(1 for entry in inventory if entry.tracked_by_git),
        "untracked_surfaces": sum(1 for entry in inventory if not entry.tracked_by_git),
        "critical_surfaces_present": missing_critical == (),
        "missing_critical_surfaces": missing_critical,
        "surfaces": paths,
    }
