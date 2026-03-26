from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


WorkloadType = Literal[
    "ui_action",
    "chat_routing",
    "automation_task",
    "heavy_inference",
    "simulation_task",
]

AllowedNodeRole = Literal[
    "mobile_node",
    "dev_node",
    "home_node",
]


@dataclass(frozen=True, slots=True)
class WorkloadPlacementRule:
    """Canonical workload placement rule."""

    workload_type: WorkloadType
    allowed_node_role: AllowedNodeRole
    preferred: bool


@dataclass(frozen=True, slots=True)
class WorkloadPlacementContract:
    """Unified workload placement matrix contract."""

    total_rules: int
    rules: tuple[WorkloadPlacementRule, ...]
