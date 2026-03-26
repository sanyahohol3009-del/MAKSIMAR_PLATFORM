from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.execution_pressure.pressure_level_models import (
    PressureLevel,
)


PressureSignalKind = Literal[
    "cpu_pressure",
    "ram_pressure",
    "queue_pressure",
    "worker_saturation",
    "artifact_storage_pressure",
]


PressureMeasurementUnit = Literal[
    "percent",
    "count",
]


@dataclass(frozen=True, slots=True)
class PressureSignalEntry:
    """Canonical pressure signal description entry."""

    signal_kind: PressureSignalKind
    measurement_unit: PressureMeasurementUnit
    elevated_threshold: int
    high_threshold: int
    critical_threshold: int
    default_level_below_elevated: PressureLevel
    description: str

    def __post_init__(self) -> None:
        """Validate signal entry invariants."""
        if not (
            self.elevated_threshold
            < self.high_threshold
            < self.critical_threshold
        ):
            raise ValueError(
                f"Invalid threshold ordering for {self.signal_kind}: "
                f"{self.elevated_threshold} < {self.high_threshold} < {self.critical_threshold} expected"
            )

        if self.measurement_unit == "percent":
            if not (
                0 <= self.elevated_threshold <= 100
                and 0 <= self.high_threshold <= 100
                and 0 <= self.critical_threshold <= 100
            ):
                raise ValueError(
                    f"Percent thresholds must be within 0–100 for {self.signal_kind}"
                )

        if self.measurement_unit == "count":
            if not (
                self.elevated_threshold >= 0
                and self.high_threshold >= 0
                and self.critical_threshold >= 0
            ):
                raise ValueError(
                    f"Count thresholds must be non-negative for {self.signal_kind}"
                )

        if self.default_level_below_elevated != "normal":
            raise ValueError(
                f"default_level_below_elevated must be 'normal' for {self.signal_kind}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.signal_kind}"
            )


@dataclass(frozen=True, slots=True)
class PressureSignalContract:
    """Unified canonical pressure signal contract."""

    total_signals: int
    signals: tuple[PressureSignalEntry, ...]


def build_pressure_signal_contract() -> PressureSignalContract:
    """Build canonical pressure signal contract."""
    signals = (
        PressureSignalEntry(
            signal_kind="cpu_pressure",
            measurement_unit="percent",
            elevated_threshold=60,
            high_threshold=80,
            critical_threshold=95,
            default_level_below_elevated="normal",
            description="CPU pressure signal derived from compute utilization.",
        ),
        PressureSignalEntry(
            signal_kind="ram_pressure",
            measurement_unit="percent",
            elevated_threshold=65,
            high_threshold=82,
            critical_threshold=95,
            default_level_below_elevated="normal",
            description="RAM pressure signal derived from system memory utilization.",
        ),
        PressureSignalEntry(
            signal_kind="queue_pressure",
            measurement_unit="count",
            elevated_threshold=4,
            high_threshold=8,
            critical_threshold=16,
            default_level_below_elevated="normal",
            description="Queue pressure signal derived from queued task backlog.",
        ),
        PressureSignalEntry(
            signal_kind="worker_saturation",
            measurement_unit="percent",
            elevated_threshold=70,
            high_threshold=85,
            critical_threshold=95,
            default_level_below_elevated="normal",
            description="Worker saturation signal derived from active concurrency saturation.",
        ),
        PressureSignalEntry(
            signal_kind="artifact_storage_pressure",
            measurement_unit="percent",
            elevated_threshold=70,
            high_threshold=85,
            critical_threshold=95,
            default_level_below_elevated="normal",
            description="Artifact storage pressure derived from persistent storage consumption.",
        ),
    )

    kinds = tuple(entry.signal_kind for entry in signals)
    if len(set(kinds)) != len(kinds):
        raise ValueError("Duplicate pressure signal kinds detected")

    return PressureSignalContract(
        total_signals=len(signals),
        signals=signals,
    )
