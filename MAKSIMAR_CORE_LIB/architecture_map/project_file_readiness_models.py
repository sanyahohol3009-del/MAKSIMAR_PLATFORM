"""Project file readiness models for MAKSIMAR roadmap control.

These models describe whether roadmap-expected files exist in the repository.
They are intentionally read-only and do not mutate project files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ALLOWED_EXPECTED_FILE_ROLES = frozenset(
    {
        "source",
        "test",
        "doc",
        "tool",
        "config",
        "runtime_state",
    }
)

ALLOWED_FILE_READINESS_STATUSES = frozenset({"EXISTS", "MISSING"})
ALLOWED_BATCH_READINESS_STATUSES = frozenset({"READY", "PARTIAL", "MISSING"})


def _validate_relative_path(value: str, field_name: str) -> None:
    if not value:
        raise ValueError(f"{field_name} must be non-empty")

    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"{field_name} must be repository-relative: {value!r}")

    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{field_name} must not contain empty/current/parent parts: {value!r}")


@dataclass(frozen=True)
class ExpectedProjectFile:
    """A roadmap-expected file entry."""

    path: str
    role: str
    required: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        _validate_relative_path(self.path, "path")

        if self.role not in ALLOWED_EXPECTED_FILE_ROLES:
            raise ValueError(f"Unsupported expected file role: {self.role!r}")

        if self.required is False and not self.description:
            raise ValueError("optional expected files require a description")


@dataclass(frozen=True)
class ProjectFileReadinessEntry:
    """Readiness state for one expected file."""

    path: str
    role: str
    status: str
    required: bool
    description: str = ""

    def __post_init__(self) -> None:
        _validate_relative_path(self.path, "path")

        if self.role not in ALLOWED_EXPECTED_FILE_ROLES:
            raise ValueError(f"Unsupported file readiness role: {self.role!r}")

        if self.status not in ALLOWED_FILE_READINESS_STATUSES:
            raise ValueError(f"Unsupported file readiness status: {self.status!r}")

    @property
    def exists(self) -> bool:
        return self.status == "EXISTS"

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "role": self.role,
            "status": self.status,
            "required": self.required,
            "description": self.description,
        }


@dataclass(frozen=True)
class ProjectBatchReadinessReport:
    """Readiness state for a roadmap batch."""

    batch_id: str
    title: str
    status: str
    expected_files: tuple[ProjectFileReadinessEntry, ...]

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id must be non-empty")

        if not self.title:
            raise ValueError("title must be non-empty")

        if self.status not in ALLOWED_BATCH_READINESS_STATUSES:
            raise ValueError(f"Unsupported batch readiness status: {self.status!r}")

        if not self.expected_files:
            raise ValueError("expected_files must be non-empty")

    @property
    def total_files(self) -> int:
        return len(self.expected_files)

    @property
    def existing_files(self) -> int:
        return sum(1 for entry in self.expected_files if entry.exists)

    @property
    def missing_required_files(self) -> tuple[str, ...]:
        return tuple(
            entry.path
            for entry in self.expected_files
            if entry.required and entry.status == "MISSING"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "batch_id": self.batch_id,
            "title": self.title,
            "status": self.status,
            "total_files": self.total_files,
            "existing_files": self.existing_files,
            "missing_required_files": list(self.missing_required_files),
            "expected_files": [entry.to_dict() for entry in self.expected_files],
        }


def build_project_batch_readiness_report(
    *,
    batch_id: str,
    title: str,
    expected_files: Iterable[ExpectedProjectFile],
    project_root: Path,
) -> ProjectBatchReadinessReport:
    """Build a deterministic read-only batch readiness report."""
    entries: list[ProjectFileReadinessEntry] = []

    for expected_file in expected_files:
        absolute_path = project_root / expected_file.path
        status = "EXISTS" if absolute_path.exists() else "MISSING"
        entries.append(
            ProjectFileReadinessEntry(
                path=expected_file.path,
                role=expected_file.role,
                status=status,
                required=expected_file.required,
                description=expected_file.description,
            )
        )

    if not entries:
        raise ValueError("expected_files must be non-empty")

    existing_count = sum(1 for entry in entries if entry.exists)
    required_missing = [
        entry for entry in entries if entry.required and entry.status == "MISSING"
    ]

    if existing_count == 0:
        status = "MISSING"
    elif required_missing:
        status = "PARTIAL"
    else:
        status = "READY"

    return ProjectBatchReadinessReport(
        batch_id=batch_id,
        title=title,
        status=status,
        expected_files=tuple(entries),
    )
