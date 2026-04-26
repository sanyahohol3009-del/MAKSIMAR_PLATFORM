from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (
    build_preview_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.rollback_readiness_contract import (
    build_rollback_readiness_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (
    build_workspace_restore_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DashboardVisibleStateEntry:
    """Canonical dashboard-visible state entry."""

    dashboard_visible_state_id: str
    workspace_id: str
    dashboard_visible_state: str
    dashboard_visible_state_class: str
    preview_surface_ready: bool
    rollback_readiness_ready: bool
    workspace_restore_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.dashboard_visible_state_id,
            "dashboard_visible_state_id",
        )
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.dashboard_visible_state, "dashboard_visible_state")
        _require_non_empty(
            self.dashboard_visible_state_class,
            "dashboard_visible_state_class",
        )
        _require_non_empty(self.description, "description")

        if self.dashboard_visible_state != "dashboard_visible_state_ready":
            raise ValueError(
                "dashboard_visible_state must remain dashboard_visible_state_ready."
            )

        if self.dashboard_visible_state_class != "main_operator_dashboard_visible_state":
            raise ValueError(
                "dashboard_visible_state_class must remain "
                "main_operator_dashboard_visible_state."
            )

        if not self.preview_surface_ready:
            raise ValueError(
                "preview_surface_ready must remain true for canonical dashboard visible state."
            )

        if not self.rollback_readiness_ready:
            raise ValueError(
                "rollback_readiness_ready must remain true for canonical dashboard visible state."
            )

        if not self.workspace_restore_ready:
            raise ValueError(
                "workspace_restore_ready must remain true for canonical dashboard visible state."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical dashboard visible state."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical dashboard visible state."
            )


@dataclass(frozen=True, slots=True)
class DashboardVisibleStateContract:
    """Canonical dashboard-visible state contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[DashboardVisibleStateEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.dashboard_visible_state == "dashboard_visible_state_ready"
        ):
            raise ValueError(
                "ready_entries must match dashboard_visible_state_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )


def build_dashboard_visible_state_contract() -> DashboardVisibleStateContract:
    """Build canonical dashboard-visible state contract."""
    preview_surface_contract = build_preview_surface_contract()
    rollback_readiness_contract = build_rollback_readiness_contract()
    workspace_restore_contract = build_workspace_restore_contract()

    workspace_id = workspace_restore_contract.entries[0].workspace_id

    entries = (
        DashboardVisibleStateEntry(
            dashboard_visible_state_id="dashboard_visible_state_001",
            workspace_id=workspace_id,
            dashboard_visible_state="dashboard_visible_state_ready",
            dashboard_visible_state_class="main_operator_dashboard_visible_state",
            preview_surface_ready=bool(preview_surface_contract.entries),
            rollback_readiness_ready=bool(rollback_readiness_contract.entries),
            workspace_restore_ready=bool(workspace_restore_contract.entries),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical dashboard visible state entry built from preview surface, "
                "rollback readiness, and workspace restore."
            ),
        ),
    )

    return DashboardVisibleStateContract(
        contract_id="dashboard_visible_state_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.dashboard_visible_state == "dashboard_visible_state_ready"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
