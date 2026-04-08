from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_render_handoff_contract import (
    build_operator_dashboard_render_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_screen_state_contract import (
    build_operator_dashboard_screen_state_contract,
)


VisibleSnapshotState = Literal[
    "visible_snapshot_ready",
]

VisibleSnapshotClass = Literal[
    "main_operator_visible_snapshot",
]

ALL_VISIBLE_SNAPSHOT_STATES: tuple[VisibleSnapshotState, ...] = (
    "visible_snapshot_ready",
)

ALL_VISIBLE_SNAPSHOT_CLASSES: tuple[VisibleSnapshotClass, ...] = (
    "main_operator_visible_snapshot",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleSnapshotEntry:
    """Canonical operator dashboard visible-snapshot entry."""

    visible_snapshot_id: str
    dashboard_id: str
    workspace_id: str
    visible_snapshot_state: VisibleSnapshotState
    visible_snapshot_class: VisibleSnapshotClass
    screen_state_ready: bool
    render_handoff_ready: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-snapshot entry."""
        _require_non_empty(self.visible_snapshot_id, "visible_snapshot_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.visible_snapshot_state not in ALL_VISIBLE_SNAPSHOT_STATES:
            raise ValueError(
                "visible_snapshot_state must be one of "
                f"{ALL_VISIBLE_SNAPSHOT_STATES}, got {self.visible_snapshot_state!r}."
            )

        if self.visible_snapshot_class not in ALL_VISIBLE_SNAPSHOT_CLASSES:
            raise ValueError(
                "visible_snapshot_class must be one of "
                f"{ALL_VISIBLE_SNAPSHOT_CLASSES}, got {self.visible_snapshot_class!r}."
            )

        if not self.screen_state_ready:
            raise ValueError(
                "screen_state_ready must remain true for canonical visible snapshot entries."
            )

        if not self.render_handoff_ready:
            raise ValueError(
                "render_handoff_ready must remain true for canonical visible snapshot entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visible snapshot entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleSnapshotContract:
    """Canonical operator dashboard visible-snapshot contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardVisibleSnapshotEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-snapshot contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.visible_snapshot_state == "visible_snapshot_ready"
        ):
            raise ValueError(
                "ready_entries must match visible_snapshot_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_visible_snapshot_contract(
) -> OperatorDashboardVisibleSnapshotContract:
    """Build canonical operator dashboard visible-snapshot contract."""
    screen_state_contract = build_operator_dashboard_screen_state_contract()
    render_handoff_contract = build_operator_dashboard_render_handoff_contract()

    screen_entry = screen_state_contract.entries[0]
    render_entry = render_handoff_contract.entries[0]

    entries = (
        OperatorDashboardVisibleSnapshotEntry(
            visible_snapshot_id="operator_dashboard_visible_snapshot_001",
            dashboard_id=screen_entry.dashboard_id,
            workspace_id=screen_entry.workspace_id,
            visible_snapshot_state="visible_snapshot_ready",
            visible_snapshot_class="main_operator_visible_snapshot",
            screen_state_ready=screen_entry.visible_state_ready,
            render_handoff_ready=(
                render_entry.render_handoff_state == "render_handoff_ready"
            ),
            operator_visible=True,
            description=(
                "Canonical visible snapshot entry assembled from operator dashboard "
                "screen state and render handoff."
            ),
        ),
    )

    return OperatorDashboardVisibleSnapshotContract(
        contract_id="operator_dashboard_visible_snapshot_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.visible_snapshot_state == "visible_snapshot_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
