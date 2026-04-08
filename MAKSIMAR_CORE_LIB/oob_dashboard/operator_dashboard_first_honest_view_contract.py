from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_snapshot_contract import (
    build_operator_dashboard_visible_snapshot_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)


HonestViewState = Literal[
    "first_honest_view_ready",
]

HonestViewClass = Literal[
    "main_operator_first_honest_view",
]

ALL_HONEST_VIEW_STATES: tuple[HonestViewState, ...] = (
    "first_honest_view_ready",
)

ALL_HONEST_VIEW_CLASSES: tuple[HonestViewClass, ...] = (
    "main_operator_first_honest_view",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstHonestViewEntry:
    """Canonical operator dashboard first honest-view entry."""

    honest_view_id: str
    dashboard_id: str
    workspace_id: str
    honest_view_state: HonestViewState
    honest_view_class: HonestViewClass
    visible_snapshot_ready: bool
    foundation_view_bound: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard first honest-view entry."""
        _require_non_empty(self.honest_view_id, "honest_view_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.honest_view_state not in ALL_HONEST_VIEW_STATES:
            raise ValueError(
                "honest_view_state must be one of "
                f"{ALL_HONEST_VIEW_STATES}, got {self.honest_view_state!r}."
            )

        if self.honest_view_class not in ALL_HONEST_VIEW_CLASSES:
            raise ValueError(
                "honest_view_class must be one of "
                f"{ALL_HONEST_VIEW_CLASSES}, got {self.honest_view_class!r}."
            )

        if not self.visible_snapshot_ready:
            raise ValueError(
                "visible_snapshot_ready must remain true for canonical first honest-view entries."
            )

        if not self.foundation_view_bound:
            raise ValueError(
                "foundation_view_bound must remain true for canonical first honest-view entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical first honest-view entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstHonestViewContract:
    """Canonical operator dashboard first honest-view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardFirstHonestViewEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard first honest-view contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.honest_view_state == "first_honest_view_ready"
        ):
            raise ValueError(
                "ready_entries must match first_honest_view_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_first_honest_view_contract(
) -> OperatorDashboardFirstHonestViewContract:
    """Build canonical operator dashboard first honest-view contract."""
    visible_snapshot_contract = build_operator_dashboard_visible_snapshot_contract()
    foundation_view_contract = build_foundation_unified_dashboard_view()

    visible_snapshot_entry = visible_snapshot_contract.entries[0]

    entries = (
        OperatorDashboardFirstHonestViewEntry(
            honest_view_id="operator_dashboard_first_honest_view_001",
            dashboard_id=visible_snapshot_entry.dashboard_id,
            workspace_id=visible_snapshot_entry.workspace_id,
            honest_view_state="first_honest_view_ready",
            honest_view_class="main_operator_first_honest_view",
            visible_snapshot_ready=(
                visible_snapshot_entry.visible_snapshot_state
                == "visible_snapshot_ready"
            ),
            foundation_view_bound=bool(foundation_view_contract),
            operator_visible=True,
            description=(
                "Canonical first honest view entry binding visible snapshot state "
                "to the foundation unified dashboard view."
            ),
        ),
    )

    return OperatorDashboardFirstHonestViewContract(
        contract_id="operator_dashboard_first_honest_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.honest_view_state == "first_honest_view_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
