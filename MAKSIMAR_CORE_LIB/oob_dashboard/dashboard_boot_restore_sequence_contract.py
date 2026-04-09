from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.input_mode_restore_contract import (
    build_input_mode_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (
    build_workspace_restore_contract,
)


DashboardBootRestoreSequenceState = Literal[
    "dashboard_boot_restore_sequence_ready",
]

DashboardBootRestoreSequenceClass = Literal[
    "dashboard_boot_restore_sequence",
]

ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_STATES: tuple[
    DashboardBootRestoreSequenceState, ...
] = (
    "dashboard_boot_restore_sequence_ready",
)

ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_CLASSES: tuple[
    DashboardBootRestoreSequenceClass, ...
] = (
    "dashboard_boot_restore_sequence",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DashboardBootRestoreSequenceEntry:
    """Canonical dashboard boot restore sequence entry."""

    dashboard_boot_restore_sequence_id: str
    workspace_id: str
    dashboard_boot_restore_sequence_state: DashboardBootRestoreSequenceState
    dashboard_boot_restore_sequence_class: DashboardBootRestoreSequenceClass
    workspace_restore_ready: bool
    input_mode_restore_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical dashboard boot restore sequence entry."""
        _require_non_empty(
            self.dashboard_boot_restore_sequence_id,
            "dashboard_boot_restore_sequence_id",
        )
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if (
            self.dashboard_boot_restore_sequence_state
            not in ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_STATES
        ):
            raise ValueError(
                "dashboard_boot_restore_sequence_state must be one of "
                f"{ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_STATES}, "
                f"got {self.dashboard_boot_restore_sequence_state!r}."
            )

        if (
            self.dashboard_boot_restore_sequence_class
            not in ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_CLASSES
        ):
            raise ValueError(
                "dashboard_boot_restore_sequence_class must be one of "
                f"{ALL_DASHBOARD_BOOT_RESTORE_SEQUENCE_CLASSES}, "
                f"got {self.dashboard_boot_restore_sequence_class!r}."
            )

        if not self.workspace_restore_ready:
            raise ValueError(
                "workspace_restore_ready must remain true for canonical "
                "dashboard boot restore sequence entries."
            )

        if not self.input_mode_restore_ready:
            raise ValueError(
                "input_mode_restore_ready must remain true for canonical "
                "dashboard boot restore sequence entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical "
                "dashboard boot restore sequence entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical dashboard boot "
                "restore sequence entries."
            )


@dataclass(frozen=True, slots=True)
class DashboardBootRestoreSequenceContract:
    """Canonical dashboard boot restore sequence contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[DashboardBootRestoreSequenceEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical dashboard boot restore sequence contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.dashboard_boot_restore_sequence_state
            == "dashboard_boot_restore_sequence_ready"
        ):
            raise ValueError(
                "ready_entries must match dashboard_boot_restore_sequence_ready count."
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


def build_dashboard_boot_restore_sequence_contract(
) -> DashboardBootRestoreSequenceContract:
    """Build canonical dashboard boot restore sequence contract."""
    workspace_restore_contract = build_workspace_restore_contract()
    input_mode_restore_contract = build_input_mode_restore_contract()

    workspace_restore_entry = workspace_restore_contract.entries[0]
    input_mode_restore_entry = input_mode_restore_contract.entries[0]

    entries = (
        DashboardBootRestoreSequenceEntry(
            dashboard_boot_restore_sequence_id=(
                "dashboard_boot_restore_sequence_001"
            ),
            workspace_id=workspace_restore_entry.workspace_id,
            dashboard_boot_restore_sequence_state=(
                "dashboard_boot_restore_sequence_ready"
            ),
            dashboard_boot_restore_sequence_class="dashboard_boot_restore_sequence",
            workspace_restore_ready=True,
            input_mode_restore_ready=(
                input_mode_restore_entry.input_mode_restore_state
                == "input_mode_restore_ready"
            ),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical dashboard boot restore sequence entry built from "
                "workspace restore and input-mode restore."
            ),
        ),
    )

    return DashboardBootRestoreSequenceContract(
        contract_id="dashboard_boot_restore_sequence_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.dashboard_boot_restore_sequence_state
            == "dashboard_boot_restore_sequence_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
