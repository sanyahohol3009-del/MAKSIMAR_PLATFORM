from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_contract import (
    build_operator_intent_contract,
)


HandoffTarget = Literal[
    "control_plane_router",
]

HandoffStatus = Literal[
    "handoff_only",
]

HandoffMode = Literal[
    "approval_gated",
    "read_only_path",
]


@dataclass(frozen=True, slots=True)
class ControlPlaneHandoffEntry:
    """Canonical control-plane handoff entry."""

    dashboard_id: str
    workspace_id: str
    handoff_target: HandoffTarget
    handoff_status: HandoffStatus
    handoff_mode: HandoffMode
    direct_execution_allowed: bool
    description: str


@dataclass(frozen=True, slots=True)
class ControlPlaneHandoffContract:
    """Canonical control-plane handoff contract."""

    total_entries: int
    approval_gated_entries: int
    read_only_path_entries: int
    entries: tuple[ControlPlaneHandoffEntry, ...]


def build_control_plane_handoff_contract() -> ControlPlaneHandoffContract:
    """Build canonical control-plane handoff contract."""
    intent_contract = build_operator_intent_contract()

    entries = tuple(
        ControlPlaneHandoffEntry(
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            handoff_target="control_plane_router",
            handoff_status="handoff_only",
            handoff_mode=(
                "approval_gated" if entry.approval_required else "read_only_path"
            ),
            direct_execution_allowed=entry.direct_execution_allowed,
            description=(
                f"Canonical control-plane handoff entry for {entry.workspace_id}."
            ),
        )
        for entry in intent_contract.entries
    )

    return ControlPlaneHandoffContract(
        total_entries=len(entries),
        approval_gated_entries=sum(
            1 for entry in entries if entry.handoff_mode == "approval_gated"
        ),
        read_only_path_entries=sum(
            1 for entry in entries if entry.handoff_mode == "read_only_path"
        ),
        entries=entries,
    )
