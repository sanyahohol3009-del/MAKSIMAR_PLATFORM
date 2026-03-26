from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BackpressureRule:
    """Canonical backpressure rule."""

    trigger_name: str
    action_name: str
    heavy_requests_blocked: bool


@dataclass(frozen=True, slots=True)
class BackpressureContract:
    """Unified backpressure contract."""

    total_rules: int
    rules: tuple[BackpressureRule, ...]
