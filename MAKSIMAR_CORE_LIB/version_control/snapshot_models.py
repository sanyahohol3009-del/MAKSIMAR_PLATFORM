from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SnapshotType = Literal[
    "manual_snapshot",
    "pre_update_snapshot",
    "conversation_snapshot",
]


@dataclass(frozen=True, slots=True)
class SnapshotRequest:
    """Canonical version-control snapshot request."""

    snapshot_id: str
    snapshot_type: SnapshotType
    approval_required: bool
    core_write_allowed: bool


@dataclass(frozen=True, slots=True)
class SnapshotRequestContract:
    """Unified snapshot request contract."""

    total_requests: int
    requests: tuple[SnapshotRequest, ...]
