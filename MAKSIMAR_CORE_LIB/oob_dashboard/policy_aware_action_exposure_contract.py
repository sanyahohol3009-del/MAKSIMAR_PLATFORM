from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PolicyAwareActionExposureEntry:
    """Canonical backward-compatible policy-aware action exposure entry."""

    exposure_id: str
    dashboard_id: str
    workspace_id: str
    panel_id: str
    action_exposure_mode: str
    action_exposure_status: str
    approval_required: bool
    direct_execution_allowed: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class PolicyAwareActionExposureContract:
    """Canonical backward-compatible policy-aware action exposure contract."""

    contract_id: str
    total_entries: int
    read_only_exposed_entries: int
    approval_gated_exposed_entries: int
    entries: Tuple[PolicyAwareActionExposureEntry, ...]
    operator_visible: bool
    description: str


def build_policy_aware_action_exposure_contract() -> PolicyAwareActionExposureContract:
    """Build canonical backward-compatible policy-aware action exposure contract."""
    entries = (
        PolicyAwareActionExposureEntry(
            exposure_id="policy_action_exposure_001",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            panel_id="panel_consistency",
            action_exposure_mode="read_only_exposed",
            action_exposure_status="visible_but_not_executed",
            approval_required=False,
            direct_execution_allowed=False,
            operator_visible=True,
            description="Canonical read-only exposure for consistency panel.",
        ),
        PolicyAwareActionExposureEntry(
            exposure_id="policy_action_exposure_002",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            panel_id="panel_diagnostics",
            action_exposure_mode="read_only_exposed",
            action_exposure_status="visible_but_not_executed",
            approval_required=False,
            direct_execution_allowed=False,
            operator_visible=True,
            description="Canonical read-only exposure for diagnostics panel.",
        ),
        PolicyAwareActionExposureEntry(
            exposure_id="policy_action_exposure_003",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            panel_id="panel_gesture_control",
            action_exposure_mode="approval_gated_exposed",
            action_exposure_status="visible_but_not_executed",
            approval_required=True,
            direct_execution_allowed=False,
            operator_visible=True,
            description="Canonical approval-gated exposure for gesture control panel.",
        ),
    )

    return PolicyAwareActionExposureContract(
        contract_id="policy_aware_action_exposure_contract_001",
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
        operator_visible=True,
        description="Canonical backward-compatible policy-aware action exposure contract.",
    )
