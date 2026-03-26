from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


LogLevel = Literal[
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]


@dataclass(frozen=True, slots=True)
class StructuredLogRecord:
    """One structured log record."""

    event_name: str
    level: LogLevel
    trace_id: str
    message: str


@dataclass(frozen=True, slots=True)
class StructuredLoggingContract:
    """Unified structured logging contract."""

    total_records: int
    records: tuple[StructuredLogRecord, ...]
