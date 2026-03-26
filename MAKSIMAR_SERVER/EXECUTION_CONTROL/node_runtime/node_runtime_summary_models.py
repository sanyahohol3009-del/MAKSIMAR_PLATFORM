from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NodeRuntimeSummaryContract:
    """Server-side read-only node runtime summary contract."""

    summary_id: str
    total_nodes: int
    gpu_enabled_nodes: int
    degraded_nodes: int
    max_queue_depth: int
    min_health_score: int
