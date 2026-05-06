from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class DedupDecision:
    file_already_imported: bool
    content_already_imported: bool
    duplicate_unit_count: int
    new_unit_count: int
    write_required: bool
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        duplicate_unit_count = _ensure_non_negative_int(
            self.duplicate_unit_count,
            "duplicate_unit_count",
        )
        new_unit_count = _ensure_non_negative_int(
            self.new_unit_count,
            "new_unit_count",
        )

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        if self.file_already_imported and self.new_unit_count > 0:
            raise ValueError(
                "file_already_imported cannot be True when new_unit_count > 0",
            )

        object.__setattr__(self, "duplicate_unit_count", duplicate_unit_count)
        object.__setattr__(self, "new_unit_count", new_unit_count)
