from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionRoute:
    """Canonical execution route."""

    request_id: str
    worker_id: str
    target_node: str
    route_allowed: bool


@dataclass(frozen=True, slots=True)
class ExecutionRouterContract:
    """Unified execution router contract."""

    total_routes: int
    routes: tuple[ExecutionRoute, ...]
