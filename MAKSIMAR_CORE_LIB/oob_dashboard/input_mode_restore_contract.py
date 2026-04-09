from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_session_restore_contract import (
    build_dashboard_session_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (
    build_panel_placement_restore_contract,
)


InputModeRestoreState = Literal[
    "input_mode_restore_ready",
]

InputModeRestoreClass = Literal[
    "dashboard_input_mode_restore",
]

InputMode = Literal[
    "operator_interaction_mode",
]

ALL_INPUT_MODE_RESTORE_STATES: tuple[InputModeRestoreState, ...] = (
    "input_mode_restore_ready",
)

ALL_INPUT_MODE_RESTORE_CLASSES: tuple[InputModeRestoreClass, ...] = (
    "dashboard_input_mode_restore",
)

ALL_INPUT_MODES: tuple[InputMode, ...] = (
    "operator_interaction_mode",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class InputModeRestoreEntry:
    """Canonical input-mode restore entry."""

    input_mode_restore_id: str
    workspace_id: str
    input_mode_restore_state: InputModeRestoreState
    input_mode_restore_class: InputModeRestoreClass
    restored_input_mode: InputMode
    dashboard_session_restore_ready: bool
    panel_placement_restore_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical input-mode restore entry."""
        _require_non_empty(self.input_mode_restore_id, "input_mode_restore_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.input_mode_restore_state not in ALL_INPUT_MODE_RESTORE_STATES:
            raise ValueError(
                "input_mode_restore_state must be one of "
                f"{ALL_INPUT_MODE_RESTORE_STATES}, "
                f"got {self.input_mode_restore_state!r}."
            )

        if self.input_mode_restore_class not in ALL_INPUT_MODE_RESTORE_CLASSES:
            raise ValueError(
                "input_mode_restore_class must be one of "
                f"{ALL_INPUT_MODE_RESTORE_CLASSES}, "
                f"got {self.input_mode_restore_class!r}."
            )

        if self.restored_input_mode not in ALL_INPUT_MODES:
            raise ValueError(
                "restored_input_mode must be one of "
                f"{ALL_INPUT_MODES}, got {self.restored_input_mode!r}."
            )

        if not self.dashboard_session_restore_ready:
            raise ValueError(
                "dashboard_session_restore_ready must remain true for canonical "
                "input-mode restore entries."
            )

        if not self.panel_placement_restore_ready:
            raise ValueError(
                "panel_placement_restore_ready must remain true for canonical "
                "input-mode restore entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical input-mode "
                "restore entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical input-mode restore entries."
            )


@dataclass(frozen=True, slots=True)
class InputModeRestoreContract:
    """Canonical input-mode restore contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[InputModeRestoreEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical input-mode restore contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.input_mode_restore_state == "input_mode_restore_ready"
        ):
            raise ValueError(
                "ready_entries must match input_mode_restore_ready count."
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


def build_input_mode_restore_contract() -> InputModeRestoreContract:
    """Build canonical input-mode restore contract."""
    dashboard_session_restore_contract = build_dashboard_session_restore_contract()
    panel_placement_restore_contract = build_panel_placement_restore_contract()

    dashboard_session_restore_entry = dashboard_session_restore_contract.entries[0]
    panel_placement_restore_entry = panel_placement_restore_contract.entries[0]

    entries = (
        InputModeRestoreEntry(
            input_mode_restore_id="input_mode_restore_001",
            workspace_id=dashboard_session_restore_entry.workspace_id,
            input_mode_restore_state="input_mode_restore_ready",
            input_mode_restore_class="dashboard_input_mode_restore",
            restored_input_mode="operator_interaction_mode",
            dashboard_session_restore_ready=True,
            panel_placement_restore_ready=(
                panel_placement_restore_entry.panel_placement_restore_state
                == "panel_placement_restore_ready"
            ),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical input-mode restore entry built from dashboard session "
                "restore and panel placement restore."
            ),
        ),
    )

    return InputModeRestoreContract(
        contract_id="input_mode_restore_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.input_mode_restore_state == "input_mode_restore_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
