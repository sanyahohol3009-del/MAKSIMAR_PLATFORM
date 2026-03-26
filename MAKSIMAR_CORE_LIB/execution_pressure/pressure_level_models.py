from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PressureLevel = Literal[
    "normal",
    "elevated",
    "high",
    "critical",
]


@dataclass(frozen=True, slots=True)
class PressureLevelEntry:
    """Canonical pressure level description entry."""

    pressure_level: PressureLevel
    severity_rank: int
    throttling_required: bool
    degraded_mode_candidate: bool
    description: str

    def __post_init__(self) -> None:
        """Validate pressure level invariants."""
        if self.severity_rank < 0:
            raise ValueError(
                f"severity_rank must be non-negative for {self.pressure_level}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.pressure_level}"
            )

        if self.pressure_level in ("high", "critical"):
            if not self.throttling_required:
                raise ValueError(
                    f"{self.pressure_level} must require throttling"
                )
            if not self.degraded_mode_candidate:
                raise ValueError(
                    f"{self.pressure_level} must be a degraded mode candidate"
                )


@dataclass(frozen=True, slots=True)
class PressureLevelContract:
    """Unified canonical pressure level contract."""

    total_levels: int
    levels: tuple[PressureLevelEntry, ...]


def build_pressure_level_contract() -> PressureLevelContract:
    """Build canonical pressure level contract."""
    levels = (
        PressureLevelEntry(
            pressure_level="normal",
            severity_rank=0,
            throttling_required=False,
            degraded_mode_candidate=False,
            description="Normal operating range with no pressure-based restrictions.",
        ),
        PressureLevelEntry(
            pressure_level="elevated",
            severity_rank=1,
            throttling_required=False,
            degraded_mode_candidate=False,
            description="Elevated pressure range that requires closer observation.",
        ),
        PressureLevelEntry(
            pressure_level="high",
            severity_rank=2,
            throttling_required=True,
            degraded_mode_candidate=True,
            description="High pressure range that may require throttling and degraded routing.",
        ),
        PressureLevelEntry(
            pressure_level="critical",
            severity_rank=3,
            throttling_required=True,
            degraded_mode_candidate=True,
            description="Critical pressure range that requires aggressive protection logic.",
        ),
    )

    level_order = tuple(entry.pressure_level for entry in levels)
    if level_order != ("normal", "elevated", "high", "critical"):
        raise ValueError("Pressure level order is invalid")

    severity_ranks = tuple(entry.severity_rank for entry in levels)
    if severity_ranks != (0, 1, 2, 3):
        raise ValueError("Pressure level severity ranks are invalid")

    if len(set(level_order)) != len(level_order):
        raise ValueError("Duplicate pressure levels detected")

    return PressureLevelContract(
        total_levels=len(levels),
        levels=levels,
    )
