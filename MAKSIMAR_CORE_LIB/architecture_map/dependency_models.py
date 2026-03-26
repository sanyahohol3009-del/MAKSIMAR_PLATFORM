from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    """Canonical dependency edge for architecture map."""

    upstream_module_id: str
    downstream_module_id: str
    critical_path: bool


@dataclass(frozen=True, slots=True)
class DependencyGraphContract:
    """Unified dependency graph contract."""

    total_edges: int
    edges: tuple[DependencyEdge, ...]
