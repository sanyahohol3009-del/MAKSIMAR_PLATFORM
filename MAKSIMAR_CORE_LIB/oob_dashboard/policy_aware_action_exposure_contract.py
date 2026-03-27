from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.control_plane_handoff_contract import (
    build_control_plane_handoff_contract,
)


ActionExposureMode = Literal[
    "read_only_exposed",
    "approval_gated_exposed",
]

ActionExposureStatus = Literal[
    "visible_but_not_executed",
]


@dataclass(frozen=True, slots=True)
class PolicyAwareActionExposureEntry:
    """Canonical policy-aware action exposure entry."""

    dashboard_id: str
    workspace_id: str
    action_exposure_mode: ActionExposureMode
    action_exposure_status: ActionExposureStatus
    direct_execution_allowed: bool
    approval_required: bool
    description: str


@dataclass(frozen=True, slots=True)
class PolicyAwareActionExposureContract:
    """Canonical policy-aware action exposure contract."""

    total_entries: int
    read_only_exposed_entries: int
    approval_gated_exposed_entries: int
    entries: tuple[PolicyAwareActionExposureEntry, ...]


def build_policy_aware_action_exposure_contract() -> (
    PolicyAwareActionExposureContract
):
    """Build canonical policy-aware action exposure contract."""
    handoff_contract = build_control_plane_handoff_contract()

    entries = tuple(
        PolicyAwareActionExposureEntry(
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            action_exposure_mode=(
                "approval_gated_exposed"
                if entry.handoff_mode == "approval_gated"
                else "read_only_exposed"
            ),
            action_exposure_status="visible_but_not_executed",
            direct_execution_allowed=entry.direct_execution_allowed,
            approval_required=(entry.handoff_mode == "approval_gated"),
            description=(
                f"Canonical policy-aware action exposure entry for {entry.workspace_id}."
            ),
        )
        for entry in handoff_contract.entries
    )

    return PolicyAwareActionExposureContract(
        total_entries=len(entries),
        read_only_exposed_entries=sum(
            1 for entry in entries if entry.action_exposure_mode == "read_only_exposed"
        ),
        approval_gated_exposed_entries=sum(
            1
            for entry in entries
            if entry.action_exposure_mode == "approval_gated_exposed"
        ),
        entries=entries,
    )
