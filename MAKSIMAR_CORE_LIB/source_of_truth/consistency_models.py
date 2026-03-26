from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConsistencyCheckLine:
    """One consistency-check line between two observability layers."""

    check_name: str
    expected_value: int
    actual_value: int
    consistent: bool


@dataclass(frozen=True, slots=True)
class ConsistencyCheckResult:
    """Unified result of one source-of-truth consistency check."""

    check_scope: str
    overall_consistent: bool
    total_lines: int
    lines: list[ConsistencyCheckLine]
