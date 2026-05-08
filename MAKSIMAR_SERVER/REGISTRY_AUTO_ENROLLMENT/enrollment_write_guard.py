from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class EnrollmentWriteGuardDecision:
    """Write guard decision for auto-enrollment artifacts."""

    target_path: str
    write_allowed: bool
    overwrite_existing: bool
    reason: str

    def __post_init__(self) -> None:
        target_path = _ensure_non_empty_str(self.target_path, "target_path")
        reason = _ensure_non_empty_str(self.reason, "reason")

        if not isinstance(self.write_allowed, bool):
            raise ValueError("write_allowed must be bool")
        if not isinstance(self.overwrite_existing, bool):
            raise ValueError("overwrite_existing must be bool")
        if self.overwrite_existing and not self.write_allowed:
            raise ValueError("overwrite_existing cannot be True when write is blocked")

        object.__setattr__(self, "target_path", target_path)
        object.__setattr__(self, "reason", reason)


def build_enrollment_write_guard_decision(
    target_path: Path,
    *,
    overwrite_existing: bool = False,
) -> EnrollmentWriteGuardDecision:
    """Build write guard decision without writing anything."""
    if target_path.exists() and not overwrite_existing:
        return EnrollmentWriteGuardDecision(
            target_path=target_path.as_posix(),
            write_allowed=False,
            overwrite_existing=False,
            reason="target_exists_no_overwrite",
        )

    return EnrollmentWriteGuardDecision(
        target_path=target_path.as_posix(),
        write_allowed=True,
        overwrite_existing=overwrite_existing,
        reason="write_allowed",
    )
