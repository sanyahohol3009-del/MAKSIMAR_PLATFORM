from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


FeatureAvailability = Literal[
    "supported",
    "degraded",
    "unsupported",
]


@dataclass(frozen=True, slots=True)
class FeatureGateEntry:
    """Canonical feature-gating decision entry."""

    node_id: CanonicalNodeId
    feature_id: str
    availability: FeatureAvailability
    reason: str


@dataclass(frozen=True, slots=True)
class FeatureGatingContract:
    """Unified feature-gating contract."""

    total_entries: int
    entries: tuple[FeatureGateEntry, ...]
