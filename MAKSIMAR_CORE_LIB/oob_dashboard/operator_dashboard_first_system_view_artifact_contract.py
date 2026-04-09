from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_final_assembled_state_contract import (
    build_operator_dashboard_final_assembled_state_contract,
)


SystemViewArtifactState = Literal[
    "system_view_artifact_ready",
]

SystemViewArtifactClass = Literal[
    "main_operator_system_view_artifact",
]

ALL_SYSTEM_VIEW_ARTIFACT_STATES: tuple[SystemViewArtifactState, ...] = (
    "system_view_artifact_ready",
)

ALL_SYSTEM_VIEW_ARTIFACT_CLASSES: tuple[SystemViewArtifactClass, ...] = (
    "main_operator_system_view_artifact",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstSystemViewArtifactEntry:
    """Canonical operator dashboard first system-view artifact entry."""

    system_view_artifact_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    system_view_artifact_state: SystemViewArtifactState
    system_view_artifact_class: SystemViewArtifactClass
    final_assembled_state_ready: bool
    operator_visible: bool
    truth_bound: bool
    read_only_boundary: bool
    oob_safe: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical first system-view artifact entry."""
        _require_non_empty(self.system_view_artifact_id, "system_view_artifact_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.system_view_artifact_state not in ALL_SYSTEM_VIEW_ARTIFACT_STATES:
            raise ValueError(
                "system_view_artifact_state must be one of "
                f"{ALL_SYSTEM_VIEW_ARTIFACT_STATES}, "
                f"got {self.system_view_artifact_state!r}."
            )

        if self.system_view_artifact_class not in ALL_SYSTEM_VIEW_ARTIFACT_CLASSES:
            raise ValueError(
                "system_view_artifact_class must be one of "
                f"{ALL_SYSTEM_VIEW_ARTIFACT_CLASSES}, "
                f"got {self.system_view_artifact_class!r}."
            )

        if not self.final_assembled_state_ready:
            raise ValueError(
                "final_assembled_state_ready must remain true for canonical "
                "system-view artifact entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical system-view "
                "artifact entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical system-view "
                "artifact entries."
            )

        if not self.read_only_boundary:
            raise ValueError(
                "read_only_boundary must remain true for canonical system-view "
                "artifact entries."
            )

        if not self.oob_safe:
            raise ValueError(
                "oob_safe must remain true for canonical system-view artifact entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstSystemViewArtifactContract:
    """Canonical operator dashboard first system-view artifact contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[OperatorDashboardFirstSystemViewArtifactEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical first system-view artifact contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.system_view_artifact_state == "system_view_artifact_ready"
        ):
            raise ValueError(
                "ready_entries must match system_view_artifact_ready count."
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
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_operator_dashboard_first_system_view_artifact_contract(
) -> OperatorDashboardFirstSystemViewArtifactContract:
    """Build canonical operator dashboard first system-view artifact contract."""
    final_assembled_state_contract = (
        build_operator_dashboard_final_assembled_state_contract()
    )
    final_assembled_state_entry = final_assembled_state_contract.entries[0]

    entries = (
        OperatorDashboardFirstSystemViewArtifactEntry(
            system_view_artifact_id=(
                "operator_dashboard_first_system_view_artifact_001"
            ),
            dashboard_id=final_assembled_state_entry.dashboard_id,
            workspace_id=final_assembled_state_entry.workspace_id,
            display_target_id=final_assembled_state_entry.display_target_id,
            system_view_artifact_state="system_view_artifact_ready",
            system_view_artifact_class="main_operator_system_view_artifact",
            final_assembled_state_ready=(
                final_assembled_state_entry.system_view_artifact_ready
            ),
            operator_visible=final_assembled_state_entry.operator_visible,
            truth_bound=final_assembled_state_entry.truth_bound,
            read_only_boundary=final_assembled_state_entry.read_only_boundary,
            oob_safe=final_assembled_state_entry.oob_safe,
            description=(
                "Canonical first system-view artifact entry built from the "
                "operator dashboard final assembled-state contract."
            ),
        ),
    )

    return OperatorDashboardFirstSystemViewArtifactContract(
        contract_id="operator_dashboard_first_system_view_artifact_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.system_view_artifact_state == "system_view_artifact_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
