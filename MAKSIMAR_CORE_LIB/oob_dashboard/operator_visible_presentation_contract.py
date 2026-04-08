from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_visual_projection_contract import (
    build_display_visual_projection_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)


PresentationState = Literal[
    "presentation_ready",
]

PresentationClass = Literal[
    "primary_operator_presentation",
    "secondary_operator_presentation",
    "tertiary_operator_presentation",
]

ALL_PRESENTATION_STATES: tuple[PresentationState, ...] = (
    "presentation_ready",
)

ALL_PRESENTATION_CLASSES: tuple[PresentationClass, ...] = (
    "primary_operator_presentation",
    "secondary_operator_presentation",
    "tertiary_operator_presentation",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorVisiblePresentationEntry:
    """Canonical operator-visible presentation entry."""

    presentation_id: str
    display_target_id: str
    interaction_surface_id: str
    presentation_state: PresentationState
    presentation_class: PresentationClass
    projection_ready: bool
    shared_surface: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator-visible presentation entry."""
        _require_non_empty(self.presentation_id, "presentation_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.interaction_surface_id, "interaction_surface_id")
        _require_non_empty(self.description, "description")

        if self.presentation_state not in ALL_PRESENTATION_STATES:
            raise ValueError(
                "presentation_state must be one of "
                f"{ALL_PRESENTATION_STATES}, got {self.presentation_state!r}."
            )

        if self.presentation_class not in ALL_PRESENTATION_CLASSES:
            raise ValueError(
                "presentation_class must be one of "
                f"{ALL_PRESENTATION_CLASSES}, got {self.presentation_class!r}."
            )

        if not self.projection_ready:
            raise ValueError(
                "projection_ready must remain true for canonical operator-visible presentation entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical operator-visible presentation entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorVisiblePresentationContract:
    """Canonical operator-visible presentation contract."""

    contract_id: str
    total_entries: int
    shared_surface_entries: int
    projection_ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorVisiblePresentationEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator-visible presentation contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.shared_surface_entries != sum(
            1 for entry in self.entries if entry.shared_surface
        ):
            raise ValueError(
                "shared_surface_entries must match shared_surface count."
            )

        if self.projection_ready_entries != sum(
            1 for entry in self.entries if entry.projection_ready
        ):
            raise ValueError(
                "projection_ready_entries must match projection_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_visible_presentation_contract() -> OperatorVisiblePresentationContract:
    """Build canonical operator-visible presentation contract."""
    projection_contract = build_display_visual_projection_contract()
    interaction_surface_contract = build_main_operator_interaction_surface_contract()

    interaction_surface_id = interaction_surface_contract.entries[0].interaction_surface_id

    presentation_class_map = {
        "display_primary_operator": "primary_operator_presentation",
        "display_secondary_diagnostics": "secondary_operator_presentation",
        "display_tertiary_expansion": "tertiary_operator_presentation",
    }

    entries = tuple(
        OperatorVisiblePresentationEntry(
            presentation_id=f"operator_visible_presentation_{index:03d}",
            display_target_id=entry.display_target_id,
            interaction_surface_id=interaction_surface_id,
            presentation_state="presentation_ready",
            presentation_class=presentation_class_map[entry.display_target_id],
            projection_ready=entry.projection_ready,
            shared_surface=entry.shared_surface,
            operator_visible=True,
            description=(
                f"Canonical operator-visible presentation entry for {entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(projection_contract.entries, start=1)
    )

    return OperatorVisiblePresentationContract(
        contract_id="operator_visible_presentation_contract_001",
        total_entries=len(entries),
        shared_surface_entries=sum(1 for entry in entries if entry.shared_surface),
        projection_ready_entries=sum(1 for entry in entries if entry.projection_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
