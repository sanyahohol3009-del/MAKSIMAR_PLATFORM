from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_honest_view_contract import (
    build_operator_dashboard_first_honest_view_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_render_handoff_contract import (
    build_operator_dashboard_render_handoff_contract,
)


VisibleOutputState = Literal[
    "visible_output_ready",
]

VisibleOutputClass = Literal[
    "main_operator_visible_output",
]

ALL_VISIBLE_OUTPUT_STATES: tuple[VisibleOutputState, ...] = (
    "visible_output_ready",
)

ALL_VISIBLE_OUTPUT_CLASSES: tuple[VisibleOutputClass, ...] = (
    "main_operator_visible_output",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleOutputEntry:
    """Canonical operator dashboard visible-output entry."""

    visible_output_id: str
    dashboard_id: str
    workspace_id: str
    visible_output_state: VisibleOutputState
    visible_output_class: VisibleOutputClass
    honest_view_ready: bool
    render_handoff_ready: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-output entry."""
        _require_non_empty(self.visible_output_id, "visible_output_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.visible_output_state not in ALL_VISIBLE_OUTPUT_STATES:
            raise ValueError(
                "visible_output_state must be one of "
                f"{ALL_VISIBLE_OUTPUT_STATES}, got {self.visible_output_state!r}."
            )

        if self.visible_output_class not in ALL_VISIBLE_OUTPUT_CLASSES:
            raise ValueError(
                "visible_output_class must be one of "
                f"{ALL_VISIBLE_OUTPUT_CLASSES}, got {self.visible_output_class!r}."
            )

        if not self.honest_view_ready:
            raise ValueError(
                "honest_view_ready must remain true for canonical visible output entries."
            )

        if not self.render_handoff_ready:
            raise ValueError(
                "render_handoff_ready must remain true for canonical visible output entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visible output entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleOutputContract:
    """Canonical operator dashboard visible-output contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardVisibleOutputEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-output contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.visible_output_state == "visible_output_ready"
        ):
            raise ValueError(
                "ready_entries must match visible_output_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_visible_output_contract(
) -> OperatorDashboardVisibleOutputContract:
    """Build canonical operator dashboard visible-output contract."""
    honest_view_contract = build_operator_dashboard_first_honest_view_contract()
    render_handoff_contract = build_operator_dashboard_render_handoff_contract()

    honest_view_entry = honest_view_contract.entries[0]
    render_handoff_entry = render_handoff_contract.entries[0]

    entries = (
        OperatorDashboardVisibleOutputEntry(
            visible_output_id="operator_dashboard_visible_output_001",
            dashboard_id=honest_view_entry.dashboard_id,
            workspace_id=honest_view_entry.workspace_id,
            visible_output_state="visible_output_ready",
            visible_output_class="main_operator_visible_output",
            honest_view_ready=(
                honest_view_entry.honest_view_state == "first_honest_view_ready"
            ),
            render_handoff_ready=(
                render_handoff_entry.render_handoff_state == "render_handoff_ready"
            ),
            operator_visible=True,
            description=(
                "Canonical operator dashboard visible-output entry assembled from "
                "the first honest view and render handoff."
            ),
        ),
    )

    return OperatorDashboardVisibleOutputContract(
        contract_id="operator_dashboard_visible_output_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.visible_output_state == "visible_output_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
