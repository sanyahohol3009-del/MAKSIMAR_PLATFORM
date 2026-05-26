"""Read-only dirty surface classifier.

This module classifies git status output. It never stages, restores, removes,
moves or commits files.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DirtySurfaceEntry:
    status_code: str
    path: str
    category: str

    def __post_init__(self) -> None:
        if not self.status_code:
            raise ValueError("status_code must not be empty")
        if not self.path:
            raise ValueError("path must not be empty")
        if self.category not in {
            "modified",
            "staged",
            "untracked",
            "deleted",
            "renamed",
            "copied",
            "mixed",
        }:
            raise ValueError(f"unsupported dirty surface category: {self.category}")


@dataclass(frozen=True, slots=True)
class DirtySurfaceClassificationResult:
    entries: tuple[DirtySurfaceEntry, ...]
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        if any(not isinstance(entry, DirtySurfaceEntry) for entry in self.entries):
            raise TypeError("entries must contain DirtySurfaceEntry values")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")

    @property
    def dirty_count(self) -> int:
        return len(self.entries)

    @property
    def untracked_count(self) -> int:
        return sum(1 for entry in self.entries if entry.category == "untracked")


def _category_from_status(status_code: str) -> str:
    if status_code == "??":
        return "untracked"
    if "R" in status_code:
        return "renamed"
    if "C" in status_code:
        return "copied"
    if "D" in status_code:
        return "deleted"
    if status_code[0] != " " and status_code[1] != " ":
        return "mixed"
    if status_code[0] != " ":
        return "staged"
    return "modified"


def classify_dirty_surfaces_from_status(status_output: str) -> DirtySurfaceClassificationResult:
    entries: list[DirtySurfaceEntry] = []

    for raw_line in status_output.splitlines():
        if not raw_line.strip():
            continue
        if len(raw_line) < 4:
            raise ValueError(f"invalid git status --short line: {raw_line!r}")

        status_code = raw_line[:2]
        path = raw_line[3:].strip()

        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()

        entries.append(
            DirtySurfaceEntry(
                status_code=status_code,
                path=path,
                category=_category_from_status(status_code),
            )
        )

    return DirtySurfaceClassificationResult(entries=tuple(entries))


def classify_dirty_surfaces(
    *,
    project_root: str | Path = ".",
) -> DirtySurfaceClassificationResult:
    completed = subprocess.run(
        ("git", "status", "--short"),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        cwd=str(project_root),
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git status --short failed")
    return classify_dirty_surfaces_from_status(completed.stdout)
