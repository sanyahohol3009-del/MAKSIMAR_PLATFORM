from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlatformSelfCheckResult:
    """Unified result of platform self-check sweep."""

    overall_status: str
    bootstrap_status: str
    health_status: str
    total_domains: int
    loaded_domains: int
    failed_domains: int
    total_items: int
