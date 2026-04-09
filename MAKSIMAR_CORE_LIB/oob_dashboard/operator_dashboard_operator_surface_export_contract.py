from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_system_view_artifact_contract import (
    build_operator_dashboard_first_system_view_artifact_contract,
)


OperatorSurfaceExportState = Literal[
    "operator_surface_export_ready",
]

OperatorSurfaceExportClass = Literal[
    "main_operator_surface_export",
]

ALL_OPERATOR_SURFACE_EXPORT_STATES: tuple[OperatorSurfaceExportState, ...] = (
    "operator_surface_export_ready",
)

ALL_OPERATOR_SURFACE_EXPORT_CLASSES: tuple[OperatorSurfaceExportClass, ...] = (
    "main_operator_surface_export",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardOperatorSurfaceExportEntry:
    """Canonical operator dashboard operator-surface export entry."""

    operator_surface_export_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    operator_surface_export_state: OperatorSurfaceExportState
    operator_surface_export_class: OperatorSurfaceExportClass
    system_view_artifact_ready: bool
    operator_visible: bool
    truth_bound: bool
    read_only_boundary: bool
    oob_safe: bool
    export_ready: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator-surface export entry."""
        _require_non_empty(self.operator_surface_export_id, "operator_surface_export_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.operator_surface_export_state not in ALL_OPERATOR_SURFACE_EXPORT_STATES:
            raise ValueError(
                "operator_surface_export_state must be one of "
                f"{ALL_OPERATOR_SURFACE_EXPORT_STATES}, "
                f"got {self.operator_surface_export_state!r}."
            )

        if self.operator_surface_export_class not in ALL_OPERATOR_SURFACE_EXPORT_CLASSES:
            raise ValueError(
                "operator_surface_export_class must be one of "
                f"{ALL_OPERATOR_SURFACE_EXPORT_CLASSES}, "
                f"got {self.operator_surface_export_class!r}."
            )

        if not self.system_view_artifact_ready:
            raise ValueError(
                "system_view_artifact_ready must remain true for canonical "
                "operator-surface export entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical operator-surface "
                "export entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical operator-surface "
                "export entries."
            )

        if not self.read_only_boundary:
            raise ValueError(
                "read_only_boundary must remain true for canonical operator-surface "
                "export entries."
            )

        if not self.oob_safe:
            raise ValueError(
                "oob_safe must remain true for canonical operator-surface export entries."
            )

        if not self.export_ready:
            raise ValueError(
                "export_ready must remain true for canonical operator-surface "
                "export entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardOperatorSurfaceExportContract:
    """Canonical operator dashboard operator-surface export contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    export_ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardOperatorSurfaceExportEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator-surface export contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.operator_surface_export_state == "operator_surface_export_ready"
        ):
            raise ValueError(
                "ready_entries must match operator_surface_export_ready count."
            )

        if self.export_ready_entries != sum(
            1 for entry in self.entries if entry.export_ready
        ):
            raise ValueError("export_ready_entries must match export_ready count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_operator_surface_export_contract(
) -> OperatorDashboardOperatorSurfaceExportContract:
    """Build canonical operator dashboard operator-surface export contract."""
    system_view_artifact_contract = (
        build_operator_dashboard_first_system_view_artifact_contract()
    )
    system_view_artifact_entry = system_view_artifact_contract.entries[0]

    entries = (
        OperatorDashboardOperatorSurfaceExportEntry(
            operator_surface_export_id="operator_dashboard_operator_surface_export_001",
            dashboard_id=system_view_artifact_entry.dashboard_id,
            workspace_id=system_view_artifact_entry.workspace_id,
            display_target_id=system_view_artifact_entry.display_target_id,
            operator_surface_export_state="operator_surface_export_ready",
            operator_surface_export_class="main_operator_surface_export",
            system_view_artifact_ready=(
                system_view_artifact_entry.system_view_artifact_state
                == "system_view_artifact_ready"
            ),
            operator_visible=system_view_artifact_entry.operator_visible,
            truth_bound=system_view_artifact_entry.truth_bound,
            read_only_boundary=system_view_artifact_entry.read_only_boundary,
            oob_safe=system_view_artifact_entry.oob_safe,
            export_ready=True,
            description=(
                "Canonical operator-surface export entry built from the first "
                "system-view artifact contract."
            ),
        ),
    )

    return OperatorDashboardOperatorSurfaceExportContract(
        contract_id="operator_dashboard_operator_surface_export_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.operator_surface_export_state == "operator_surface_export_ready"
        ),
        export_ready_entries=sum(1 for entry in entries if entry.export_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
