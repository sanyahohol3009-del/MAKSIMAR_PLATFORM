from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
    PayloadDirection,
)


ArtifactRoutingBindingStatus = Literal[
    "inline_control_route",
    "bound_to_data_plane",
    "rejected",
]


@dataclass(frozen=True, slots=True)
class ArtifactRoutingBindingEntry:
    """Server-side artifact routing binding entry."""

    request_id: str
    detected_payload_class: PayloadClass
    route_target: PayloadDirection
    artifact_ref: str
    owner_task_id: str
    binding_status: ArtifactRoutingBindingStatus
    artifact_declared: bool
    binding_reason: str


@dataclass(frozen=True, slots=True)
class ArtifactRoutingBindingContract:
    """Unified server-side artifact routing binding contract."""

    total_entries: int
    entries: tuple[ArtifactRoutingBindingEntry, ...]
