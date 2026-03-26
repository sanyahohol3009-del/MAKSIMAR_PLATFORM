from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlatformHealthDomain:
    """Health state for one platform domain."""

    domain_name: str
    total_items: int
    is_loaded: bool
    status: str


@dataclass(frozen=True, slots=True)
class PlatformHealthSnapshot:
    """Unified health snapshot for the platform."""

    overall_status: str
    total_domains: int
    loaded_domains: int
    failed_domains: int
    total_items: int
