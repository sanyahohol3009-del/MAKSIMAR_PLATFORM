from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_real_picture_contract import (
    build_operator_dashboard_first_real_picture_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_output_contract import (
    build_operator_dashboard_visible_output_contract,
)


FinalAssembledState = Literal[
    "final_assembled_state_ready",
]

FinalAssembledClass = Literal[
    "main_operator_final_assembled_state",
]

ALL_FINAL_ASSEMBLED_STATES: tuple[FinalAssembledState, ...] = (
    "final_assembled_state_ready",
)

ALL_FINAL_ASSEMBLED_CLASSES: tuple[FinalAssembledClass, ...] = (
    "main_operator_final_assembled_state",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardFinalAssembledStateEntry:
    """Canonical operator dashboard final assembled-state entry."""

    assembled_state_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    assembled_state: FinalAssembledState
    assembled_class: FinalAssembledClass
    interaction_surface_ready: bool
    visible_output_ready: bool
    first_real_picture_ready: bool
    system_view_artifact_ready: bool
    operator_visible: bool
    truth_bound: bool
    read_only_boundary: bool
    oob_safe: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard final assembled-state entry."""
        _require_non_empty(self.assembled_state_id, "assembled_state_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.assembled_state not in ALL_FINAL_ASSEMBLED_STATES:
            raise ValueError(
                "assembled_state must be one of "
                f"{ALL_FINAL_ASSEMBLED_STATES}, got {self.assembled_state!r}."
            )

        if self.assembled_class not in ALL_FINAL_ASSEMBLED_CLASSES:
            raise ValueError(
                "assembled_class must be one of "
                f"{ALL_FINAL_ASSEMBLED_CLASSES}, got {self.assembled_class!r}."
            )

        if not self.interaction_surface_ready:
            raise ValueError(
                "interaction_surface_ready must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.visible_output_ready:
            raise ValueError(
                "visible_output_ready must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.first_real_picture_ready:
            raise ValueError(
                "first_real_picture_ready must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.system_view_artifact_ready:
            raise ValueError(
                "system_view_artifact_ready must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical final assembled-state "
                "entries."
            )

        if not self.read_only_boundary:
            raise ValueError(
                "read_only_boundary must remain true for canonical final "
                "assembled-state entries."
            )

        if not self.oob_safe:
            raise ValueError(
                "oob_safe must remain true for canonical final assembled-state entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardFinalAssembledStateContract:
    """Canonical operator dashboard final assembled-state contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    system_view_artifact_ready_entries: int
    entries: tuple[OperatorDashboardFinalAssembledStateEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard final assembled-state contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.assembled_state == "final_assembled_state_ready"
        ):
            raise ValueError(
                "ready_entries must match final_assembled_state_ready count."
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

        if self.system_view_artifact_ready_entries != sum(
            1 for entry in self.entries if entry.system_view_artifact_ready
        ):
            raise ValueError(
                "system_view_artifact_ready_entries must match "
                "system_view_artifact_ready count."
            )


def build_operator_dashboard_final_assembled_state_contract(
) -> OperatorDashboardFinalAssembledStateContract:
    """Build canonical operator dashboard final assembled-state contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    interaction_surface_contract = build_main_operator_interaction_surface_contract()
    visible_output_contract = build_operator_dashboard_visible_output_contract()
    first_real_picture_contract = build_operator_dashboard_first_real_picture_contract()

    dashboard_entry = dashboard_contract.entries[0]
    interaction_surface_entry = interaction_surface_contract.entries[0]
    visible_output_entry = visible_output_contract.entries[0]
    first_real_picture_entry = first_real_picture_contract.entries[0]

    interaction_surface_ready = (
        interaction_surface_entry.interaction_surface_status
        == "interaction_surface_assembled"
    )
    visible_output_ready = (
        visible_output_entry.visible_output_state == "visible_output_ready"
    )
    first_real_picture_ready = (
        first_real_picture_entry.first_real_picture_state
        == "first_real_picture_ready"
    )

    entries = (
        OperatorDashboardFinalAssembledStateEntry(
            assembled_state_id="operator_dashboard_final_assembled_state_001",
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            display_target_id=dashboard_entry.display_target_id,
            assembled_state="final_assembled_state_ready",
            assembled_class="main_operator_final_assembled_state",
            interaction_surface_ready=interaction_surface_ready,
            visible_output_ready=visible_output_ready,
            first_real_picture_ready=first_real_picture_ready,
            system_view_artifact_ready=(
                interaction_surface_ready
                and visible_output_ready
                and first_real_picture_ready
            ),
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=True,
            description=(
                "Canonical operator dashboard final assembled-state entry built from "
                "the main operator dashboard, interaction surface, visible output, "
                "and first real picture contracts."
            ),
        ),
    )

    return OperatorDashboardFinalAssembledStateContract(
        contract_id="operator_dashboard_final_assembled_state_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.assembled_state == "final_assembled_state_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        system_view_artifact_ready_entries=sum(
            1 for entry in entries if entry.system_view_artifact_ready
        ),
        entries=entries,
    )
