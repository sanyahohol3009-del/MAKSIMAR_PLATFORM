from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DataPlaneShellContract:
    """Final shell contract for data plane / artifact layer."""

    shell_id: str
    total_ownership_entries: int
    total_retention_rules: int
    total_cleanup_rules: int
