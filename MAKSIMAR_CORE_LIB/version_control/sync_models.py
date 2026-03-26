from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SyncStateType = Literal[
    "clean",
    "pending_changes",
    "ahead_of_remote",
    "behind_remote",
]


@dataclass(frozen=True, slots=True)
class SyncState:
    """Canonical version-control sync state."""

    repo_id: str
    branch_name: str
    sync_state: SyncStateType
    approval_required_for_push: bool


@dataclass(frozen=True, slots=True)
class SyncStateContract:
    """Unified sync state contract."""

    total_repos: int
    repos: tuple[SyncState, ...]
