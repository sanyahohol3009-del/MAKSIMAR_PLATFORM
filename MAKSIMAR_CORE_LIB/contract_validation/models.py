from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


IssueLevel = Literal["error", "warning"]


@dataclass(slots=True, frozen=True)
class ContractIssue:
    """Single validation issue produced by the engine."""

    file_path: Path
    path: str
    level: IssueLevel
    message: str


@dataclass(slots=True)
class ContractCheckResult:
    """Validation result for one contract file."""

    file_path: Path
    contract_name: str | None = None
    schema_version: str | None = None
    is_valid: bool = True
    issues: list[ContractIssue] = field(default_factory=list)

    def add_error(self, path: str, message: str) -> None:
        """Append validation error and mark result invalid."""
        self.is_valid = False
        self.issues.append(
            ContractIssue(
                file_path=self.file_path,
                path=path,
                level="error",
                message=message,
            )
        )

    def add_warning(self, path: str, message: str) -> None:
        """Append validation warning."""
        self.issues.append(
            ContractIssue(
                file_path=self.file_path,
                path=path,
                level="warning",
                message=message,
            )
        )


@dataclass(slots=True, frozen=True)
class ContractDocument:
    """Loaded contract document before validation."""

    file_path: Path
    payload: dict[str, object]


@dataclass(slots=True)
class ValidationSummary:
    """Aggregated summary across all validated contracts."""

    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0
    warning_count: int = 0
    error_count: int = 0

    def register_result(self, result: ContractCheckResult) -> None:
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
