"""Pytest full-platform report gate for MAKSIMAR.

Target pytest runs must stay quiet. Full reports are allowed only when the
operator explicitly enables the full-platform report mode.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


FULL_PLATFORM_REPORTS_ENV = "MAKSIMAR_FULL_PLATFORM_REPORTS"
FULL_PLATFORM_REPORTS_OPTION = "--maksimar-full-platform-reports"
FULL_PLATFORM_REPORTS_OPTION_NAME = "maksimar_full_platform_reports"


@dataclass(frozen=True)
class PytestReportGateDecision:
    """Report gate decision for pytest terminal summaries."""

    full_reports_enabled: bool
    source: str

    def __post_init__(self) -> None:
        if self.source not in {"env", "pytest_option", "disabled"}:
            raise ValueError(f"Unsupported report gate source: {self.source!r}")

        if self.source == "disabled" and self.full_reports_enabled:
            raise ValueError("disabled report gate cannot enable full reports")

        if self.source in {"env", "pytest_option"} and not self.full_reports_enabled:
            raise ValueError("enabled source must enable full reports")


def _get_pytest_option(config: Any) -> bool:
    """Read pytest option safely from config-like objects."""
    getter = getattr(config, "getoption", None)
    if not callable(getter):
        return False

    try:
        return bool(getter(FULL_PLATFORM_REPORTS_OPTION_NAME, default=False))
    except TypeError:
        try:
            return bool(getter(FULL_PLATFORM_REPORTS_OPTION_NAME))
        except Exception:
            return False
    except Exception:
        return False


def get_pytest_report_gate_decision(config: Any | None = None) -> PytestReportGateDecision:
    """Return whether full-platform pytest reports are enabled."""
    if os.environ.get(FULL_PLATFORM_REPORTS_ENV) == "1":
        return PytestReportGateDecision(full_reports_enabled=True, source="env")

    if config is not None and _get_pytest_option(config):
        return PytestReportGateDecision(
            full_reports_enabled=True,
            source="pytest_option",
        )

    return PytestReportGateDecision(full_reports_enabled=False, source="disabled")


def is_maksimar_full_platform_report_enabled(config: Any | None = None) -> bool:
    """Return True only when full-platform pytest reports are explicitly enabled."""
    return get_pytest_report_gate_decision(config).full_reports_enabled
