from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


IssueLevel = Literal["error", "warning"]


@dataclass(slots=True, frozen=True)
class ConfigIssue:
    """Single config loading or validation issue."""

    file_path: Path
    path: str
    level: IssueLevel
    message: str


@dataclass(slots=True, frozen=True)
class ConfigDocument:
    """Loaded config document."""

    file_path: Path
    schema_version: str | None
    payload: dict[str, object]


@dataclass(slots=True)
class ConfigLoadResult:
    """Per-file config load result."""

    file_path: Path
    schema_version: str | None = None
    payload: dict[str, object] | None = None
    is_valid: bool = True
    issues: list[ConfigIssue] = field(default_factory=list)

    def add_error(self, path: str, message: str) -> None:
        """Append error and mark result invalid."""
        self.is_valid = False
        self.issues.append(
            ConfigIssue(
                file_path=self.file_path,
                path=path,
                level="error",
                message=message,
            )
        )

    def add_warning(self, path: str, message: str) -> None:
        """Append warning."""
        self.issues.append(
            ConfigIssue(
                file_path=self.file_path,
                path=path,
                level="warning",
                message=message,
            )
        )


@dataclass(slots=True)
class ConfigLoadSummary:
    """Aggregated summary across loaded config files."""

    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0
    warning_count: int = 0
    error_count: int = 0

    def register_result(self, result: ConfigLoadResult) -> None:
        """Accumulate counters from one result."""
        self.total_files += 1
        if result.is_valid:
            self.valid_files += 1
        else:
            self.invalid_files += 1

        for issue in result.issues:
            if issue.level == "warning":
                self.warning_count += 1
            elif issue.level == "error":
                self.error_count += 1
