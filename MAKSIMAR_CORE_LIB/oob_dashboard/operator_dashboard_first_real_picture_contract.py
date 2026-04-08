from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_output_contract import (
    build_operator_dashboard_visible_output_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_screen_contract import (
    build_visual_hud_screen_contract,
)


FirstRealPictureState = Literal[
    "first_real_picture_ready",
]

FirstRealPictureClass = Literal[
    "main_operator_first_real_picture",
]

ALL_FIRST_REAL_PICTURE_STATES: tuple[FirstRealPictureState, ...] = (
    "first_real_picture_ready",
)

ALL_FIRST_REAL_PICTURE_CLASSES: tuple[FirstRealPictureClass, ...] = (
    "main_operator_first_real_picture",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstRealPictureEntry:
    """Canonical operator dashboard first real-picture entry."""

    first_real_picture_id: str
    dashboard_id: str
    workspace_id: str
    first_real_picture_state: FirstRealPictureState
    first_real_picture_class: FirstRealPictureClass
    visible_output_ready: bool
    hud_screen_bound: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard first real-picture entry."""
        _require_non_empty(self.first_real_picture_id, "first_real_picture_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.first_real_picture_state not in ALL_FIRST_REAL_PICTURE_STATES:
            raise ValueError(
                "first_real_picture_state must be one of "
                f"{ALL_FIRST_REAL_PICTURE_STATES}, got {self.first_real_picture_state!r}."
            )

        if self.first_real_picture_class not in ALL_FIRST_REAL_PICTURE_CLASSES:
            raise ValueError(
                "first_real_picture_class must be one of "
                f"{ALL_FIRST_REAL_PICTURE_CLASSES}, got {self.first_real_picture_class!r}."
            )

        if not self.visible_output_ready:
            raise ValueError(
                "visible_output_ready must remain true for canonical first real-picture entries."
            )

        if not self.hud_screen_bound:
            raise ValueError(
                "hud_screen_bound must remain true for canonical first real-picture entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical first real-picture entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstRealPictureContract:
    """Canonical operator dashboard first real-picture contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardFirstRealPictureEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard first real-picture contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.first_real_picture_state == "first_real_picture_ready"
        ):
            raise ValueError(
                "ready_entries must match first_real_picture_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_first_real_picture_contract(
) -> OperatorDashboardFirstRealPictureContract:
    """Build canonical operator dashboard first real-picture contract."""
    visible_output_contract = build_operator_dashboard_visible_output_contract()
    hud_screen_contract = build_visual_hud_screen_contract()

    visible_output_entry = visible_output_contract.entries[0]

    entries = (
        OperatorDashboardFirstRealPictureEntry(
            first_real_picture_id="operator_dashboard_first_real_picture_001",
            dashboard_id=visible_output_entry.dashboard_id,
            workspace_id=visible_output_entry.workspace_id,
            first_real_picture_state="first_real_picture_ready",
            first_real_picture_class="main_operator_first_real_picture",
            visible_output_ready=(
                visible_output_entry.visible_output_state == "visible_output_ready"
            ),
            hud_screen_bound=bool(hud_screen_contract),
            operator_visible=True,
            description=(
                "Canonical first real picture entry binding visible output to "
                "the visual HUD screen contract."
            ),
        ),
    )

    return OperatorDashboardFirstRealPictureContract(
        contract_id="operator_dashboard_first_real_picture_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.first_real_picture_state == "first_real_picture_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
