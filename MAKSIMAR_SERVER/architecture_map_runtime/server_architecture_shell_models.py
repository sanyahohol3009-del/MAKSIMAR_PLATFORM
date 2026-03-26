from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerArchitectureMapShellContract:
    """Final shell contract for server-side architecture map layer."""

    shell_id: str
    total_module_views: int
    total_dependency_views: int
    total_flow_views: int
