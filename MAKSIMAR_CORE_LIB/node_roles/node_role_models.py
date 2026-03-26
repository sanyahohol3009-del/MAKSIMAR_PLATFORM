from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


NodeRoleType = Literal[
    "mobile_node",
    "dev_node",
    "home_node",
]


@dataclass(frozen=True, slots=True)
class NodeRole:
    """Canonical node role definition."""

    node_id: str
    role_type: NodeRoleType
    core_write_allowed: bool
    heavy_execution_allowed: bool
    security_root: bool


@dataclass(frozen=True, slots=True)
class NodeRoleContract:
    """Unified node role contract."""

    total_nodes: int
    nodes: tuple[NodeRole, ...]
