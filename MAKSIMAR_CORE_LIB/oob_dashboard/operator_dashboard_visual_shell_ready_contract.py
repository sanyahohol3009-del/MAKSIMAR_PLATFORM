from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_operator_surface_export_contract import (
    build_operator_dashboard_operator_surface_export_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import (
    build_visual_shell_contract,
)


VisualShellReadyState = Literal[
    "visual_shell_ready",
]

VisualShellReadyClass = Literal[
    "main_operator_visual_shell_ready",
]

ALL_VISUAL_SHELL_READY_STATES: tuple[VisualShellReadyState, ...] = (
    "visual_shell_ready",
)

ALL_VISUAL_SHELL_READY_CLASSES: tuple[VisualShellReadyClass, ...] = (
    "main_operator_visual_shell_ready",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisualShellReadyEntry:
    """Canonical operator dashboard visual-shell-ready entry."""

    visual_shell_ready_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    visual_shell_ready_state: VisualShellReadyState
    visual_shell_ready_class: VisualShellReadyClass
    operator_surface_export_ready: bool
    visual_shell_bound: bool
    operator_visible: bool
    truth_bound: bool
    read_only_boundary: bool
    oob_safe: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical visual-shell-ready entry."""
        _require_non_empty(self.visual_shell_ready_id, "visual_shell_ready_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.visual_shell_ready_state not in ALL_VISUAL_SHELL_READY_STATES:
            raise ValueError(
                "visual_shell_ready_state must be one of "
                f"{ALL_VISUAL_SHELL_READY_STATES}, "
                f"got {self.visual_shell_ready_state!r}."
            )

        if self.visual_shell_ready_class not in ALL_VISUAL_SHELL_READY_CLASSES:
            raise ValueError(
                "visual_shell_ready_class must be one of "
                f"{ALL_VISUAL_SHELL_READY_CLASSES}, "
                f"got {self.visual_shell_ready_class!r}."
            )

        if not self.operator_surface_export_ready:
            raise ValueError(
                "operator_surface_export_ready must remain true for canonical "
                "visual-shell-ready entries."
            )

        if not self.visual_shell_bound:
            raise ValueError(
                "visual_shell_bound must remain true for canonical "
                "visual-shell-ready entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical "
                "visual-shell-ready entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual-shell-ready entries."
            )

        if not self.read_only_boundary:
            raise ValueError(
                "read_only_boundary must remain true for canonical "
                "visual-shell-ready entries."
            )

        if not self.oob_safe:
            raise ValueError(
                "oob_safe must remain true for canonical visual-shell-ready entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisualShellReadyContract:
    """Canonical operator dashboard visual-shell-ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    shell_bound_entries: int
    entries: tuple[OperatorDashboardVisualShellReadyEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical visual-shell-ready contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.visual_shell_ready_state == "visual_shell_ready"
        ):
            raise ValueError("ready_entries must match visual_shell_ready count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.shell_bound_entries != sum(
            1 for entry in self.entries if entry.visual_shell_bound
        ):
            raise ValueError("shell_bound_entries must match visual_shell_bound count.")


def build_operator_dashboard_visual_shell_ready_contract(
) -> OperatorDashboardVisualShellReadyContract:
    """Build canonical operator dashboard visual-shell-ready contract."""
    operator_surface_export_contract = (
        build_operator_dashboard_operator_surface_export_contract()
    )
    visual_shell_contract = build_visual_shell_contract()

    operator_surface_export_entry = operator_surface_export_contract.entries[0]

    entries = (
        OperatorDashboardVisualShellReadyEntry(
            visual_shell_ready_id="operator_dashboard_visual_shell_ready_001",
            dashboard_id=operator_surface_export_entry.dashboard_id,
            workspace_id=operator_surface_export_entry.workspace_id,
            display_target_id=operator_surface_export_entry.display_target_id,
            visual_shell_ready_state="visual_shell_ready",
            visual_shell_ready_class="main_operator_visual_shell_ready",
            operator_surface_export_ready=(
                operator_surface_export_entry.operator_surface_export_state
                == "operator_surface_export_ready"
            ),
            visual_shell_bound=bool(visual_shell_contract),
            operator_visible=operator_surface_export_entry.operator_visible,
            truth_bound=operator_surface_export_entry.truth_bound,
            read_only_boundary=operator_surface_export_entry.read_only_boundary,
            oob_safe=operator_surface_export_entry.oob_safe,
            description=(
                "Canonical visual-shell-ready entry built from the operator-surface "
                "export contract and the visual shell contract."
            ),
        ),
    )

    return OperatorDashboardVisualShellReadyContract(
        contract_id="operator_dashboard_visual_shell_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.visual_shell_ready_state == "visual_shell_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        shell_bound_entries=sum(1 for entry in entries if entry.visual_shell_bound),
        entries=entries,
    )
