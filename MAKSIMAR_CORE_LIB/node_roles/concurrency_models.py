from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConcurrencyRule:
    """Canonical concurrency control rule."""

    resource_type: str
    single_writer: bool
    max_parallel_tasks: int


@dataclass(frozen=True, slots=True)
class ConcurrencyContract:
    """Unified concurrency guard contract."""

    total_rules: int
    rules: tuple[ConcurrencyRule, ...]
