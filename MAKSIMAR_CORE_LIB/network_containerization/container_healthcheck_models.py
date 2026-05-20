from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ContainerHealthcheckModel:
    enabled: bool
    command: tuple[str, ...]
    interval_seconds: int
    timeout_seconds: int
    retries: int
    start_period_seconds: int
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_true("enabled", self.enabled)
        _validate_command(self.command)
        _validate_positive("interval_seconds", self.interval_seconds)
        _validate_positive("timeout_seconds", self.timeout_seconds)
        _validate_positive("retries", self.retries)
        _validate_non_negative("start_period_seconds", self.start_period_seconds)
        if self.timeout_seconds >= self.interval_seconds:
            raise ValueError("timeout_seconds must be lower than interval_seconds")
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "command": self.command,
            "interval_seconds": self.interval_seconds,
            "timeout_seconds": self.timeout_seconds,
            "retries": self.retries,
            "start_period_seconds": self.start_period_seconds,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_default_container_healthcheck_model() -> ContainerHealthcheckModel:
    return ContainerHealthcheckModel(
        enabled=True,
        command=("CMD", "python", "-c", "print('healthcheck')"),
        interval_seconds=30,
        timeout_seconds=5,
        retries=3,
        start_period_seconds=10,
        dashboard_safe=True,
        reason_codes=("healthcheck_required", "dashboard_safe_healthcheck_read_model"),
    )


def _validate_command(command: tuple[str, ...]) -> None:
    if not isinstance(command, tuple):
        raise TypeError("command must be a tuple")
    if not command:
        raise ValueError("command must not be empty")
    for item in command:
        if not isinstance(item, str) or not item:
            raise ValueError("command items must be non-empty strings")


def _validate_positive(field_name: str, value: int) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")


def _validate_non_negative(field_name: str, value: int) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must not be negative")


def _validate_true(field_name: str, value: bool) -> None:
    if not value:
        raise ValueError(f"{field_name} must remain true")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
