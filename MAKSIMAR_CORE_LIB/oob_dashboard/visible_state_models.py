from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


VisibleStateState = Literal[
    "visible_state_ready",
]

VisibleStateClass = Literal[
    "foundation_visible_state",
    "interaction_visible_state",
]

VisibleStateMode = Literal[
    "assembled_foundation_visible_state",
    "assembled_interaction_visible_state",
]

ALL_VISIBLE_STATE_STATES: tuple[VisibleStateState, ...] = (
    "visible_state_ready",
)

ALL_VISIBLE_STATE_CLASSES: tuple[VisibleStateClass, ...] = (
    "foundation_visible_state",
    "interaction_visible_state",
)

ALL_VISIBLE_STATE_MODES: tuple[VisibleStateMode, ...] = (
    "assembled_foundation_visible_state",
    "assembled_interaction_visible_state",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisibleStateEntry:
    """Canonical visible state entry."""

    visible_state_id: str
    display_target_id: str
    workspace_id: str
    visible_state_state: VisibleStateState
    visible_state_class: VisibleStateClass
    visible_state_mode: VisibleStateMode
    final_visible_screen_state_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.visible_state_id, "visible_state_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.visible_state_state not in ALL_VISIBLE_STATE_STATES:
            raise ValueError(
                "visible_state_state must be one of "
                f"{ALL_VISIBLE_STATE_STATES}, got {self.visible_state_state!r}."
            )

        if self.visible_state_class not in ALL_VISIBLE_STATE_CLASSES:
            raise ValueError(
                "visible_state_class must be one of "
                f"{ALL_VISIBLE_STATE_CLASSES}, got {self.visible_state_class!r}."
            )

        if self.visible_state_mode not in ALL_VISIBLE_STATE_MODES:
            raise ValueError(
                "visible_state_mode must be one of "
                f"{ALL_VISIBLE_STATE_MODES}, got {self.visible_state_mode!r}."
            )

        if not self.final_visible_screen_state_ready:
            raise ValueError(
                "final_visible_screen_state_ready must remain true for canonical visible state entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visible state entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visible state entries."
            )

        if (
            self.visible_state_class == "foundation_visible_state"
            and self.visible_state_mode != "assembled_foundation_visible_state"
        ):
            raise ValueError(
                "foundation_visible_state must use assembled_foundation_visible_state."
            )

        if (
            self.visible_state_class == "interaction_visible_state"
            and self.visible_state_mode != "assembled_interaction_visible_state"
        ):
            raise ValueError(
                "interaction_visible_state must use assembled_interaction_visible_state."
            )


@dataclass(frozen=True, slots=True)
class VisibleStateContract:
    """Canonical visible state contract."""

    contract_id: str
    total_entries: int
    foundation_visible_entries: int
    interaction_visible_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VisibleStateEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_visible_entries != sum(
            1
            for entry in self.entries
            if entry.visible_state_class == "foundation_visible_state"
        ):
            raise ValueError(
                "foundation_visible_entries must match foundation_visible_state count."
            )

        if self.interaction_visible_entries != sum(
            1
            for entry in self.entries
            if entry.visible_state_class == "interaction_visible_state"
        ):
            raise ValueError(
                "interaction_visible_entries must match interaction_visible_state count."
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
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )
