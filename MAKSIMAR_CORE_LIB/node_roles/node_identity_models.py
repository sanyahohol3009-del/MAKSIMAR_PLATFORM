from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CanonicalNodeId = Literal[
    "mobile_001",
    "dev_001",
    "home_001",
]

CanonicalNodeType = Literal[
    "mobile_node",
    "dev_node",
    "home_node",
]


@dataclass(frozen=True, slots=True)
class CanonicalNodeIdentity:
    """Canonical node identity entry."""

    node_id: CanonicalNodeId
    node_type: CanonicalNodeType


@dataclass(frozen=True, slots=True)
class CanonicalNodeIdentityContract:
    """Unified canonical node identity contract."""

    total_nodes: int
    nodes: tuple[CanonicalNodeIdentity, ...]
