from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
)


InteractionSurfaceMode = Literal[
    "read_only_operator_surface",
    "approval_bound_operator_surface",
]

InteractionSurfaceStatus = Literal[
    "interaction_surface_assembled",
]

ALL_INTERACTION_SURFACE_MODES: tuple[InteractionSurfaceMode, ...] = (
    "read_only_operator_surface",
    "approval_bound_operator_surface",
)

ALL_INTERACTION_SURFACE_STATUSES: tuple[InteractionSurfaceStatus, ...] = (
    "interaction_surface_assembled",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MainOperatorInteractionSurfaceEntry:
    """Canonical main-operator interaction surface entry."""

    interaction_surface_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    interaction_surface_mode: InteractionSurfaceMode
    interaction_surface_status: InteractionSurfaceStatus
    total_interaction_entries: int
    read_only_lane_entries: int
    approval_bound_lane_entries: int
    handoff_ready_entries: int
    operator_visible: bool
    read_only_surface: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical main-operator interaction surface entry."""
        _require_non_empty(self.interaction_surface_id, "interaction_surface_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.interaction_surface_mode not in ALL_INTERACTION_SURFACE_MODES:
            raise ValueError(
                "interaction_surface_mode must be one of "
                f"{ALL_INTERACTION_SURFACE_MODES}, got {self.interaction_surface_mode!r}."
            )

        if self.interaction_surface_status not in ALL_INTERACTION_SURFACE_STATUSES:
            raise ValueError(
                "interaction_surface_status must be one of "
                f"{ALL_INTERACTION_SURFACE_STATUSES}, got {self.interaction_surface_status!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical interaction surfaces."
            )

        if self.interaction_surface_mode == "read_only_operator_surface":
            if not self.read_only_surface:
                raise ValueError(
                    "read_only_operator_surface entries must mark read_only_surface=True."
                )

        if self.interaction_surface_mode == "approval_bound_operator_surface":
            if self.read_only_surface:
                raise ValueError(
                    "approval_bound_operator_surface entries must not mark read_only_surface=True."
                )


@dataclass(frozen=True, slots=True)
class MainOperatorInteractionSurfaceContract:
    """Canonical main-operator interaction surface contract."""

    contract_id: str
    total_entries: int
    read_only_surface_entries: int
    approval_bound_surface_entries: int
    operator_visible_entries: int
    entries: tuple[MainOperatorInteractionSurfaceEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical main-operator interaction surface contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.read_only_surface_entries != sum(
            1
            for entry in self.entries
            if entry.interaction_surface_mode == "read_only_operator_surface"
        ):
            raise ValueError(
                "read_only_surface_entries must match read_only_operator_surface count."
            )

        if self.approval_bound_surface_entries != sum(
            1
            for entry in self.entries
            if entry.interaction_surface_mode == "approval_bound_operator_surface"
        ):
            raise ValueError(
                "approval_bound_surface_entries must match approval_bound_operator_surface count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_main_operator_interaction_surface_contract() -> MainOperatorInteractionSurfaceContract:
    """Build canonical main-operator interaction surface contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    interaction_read_model = build_operator_interaction_read_model_contract()

    dashboard_entry = dashboard_contract.entries[0]

    read_only_count = interaction_read_model.read_only_lane_entries
    approval_bound_count = interaction_read_model.approval_bound_lane_entries

    entries = (
        MainOperatorInteractionSurfaceEntry(
            interaction_surface_id="main_operator_interaction_surface_001",
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            display_target_id=dashboard_entry.display_target_id,
            interaction_surface_mode="approval_bound_operator_surface",
            interaction_surface_status="interaction_surface_assembled",
            total_interaction_entries=interaction_read_model.total_entries,
            read_only_lane_entries=read_only_count,
            approval_bound_lane_entries=approval_bound_count,
            handoff_ready_entries=interaction_read_model.handoff_ready_entries,
            operator_visible=True,
            read_only_surface=False,
            description=(
                "Canonical main-operator interaction surface assembled from "
                "read-only and approval-bound operator interaction read-model lanes."
            ),
        ),
    )

    return MainOperatorInteractionSurfaceContract(
        contract_id="main_operator_interaction_surface_contract_001",
        total_entries=len(entries),
        read_only_surface_entries=sum(
            1
            for entry in entries
            if entry.interaction_surface_mode == "read_only_operator_surface"
        ),
        approval_bound_surface_entries=sum(
            1
            for entry in entries
            if entry.interaction_surface_mode == "approval_bound_operator_surface"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
