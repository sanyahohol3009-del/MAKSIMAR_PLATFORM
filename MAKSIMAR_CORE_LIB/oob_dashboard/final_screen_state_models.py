from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FinalScreenStateState = Literal[
    "final_screen_state_ready",
]

FinalScreenStateClass = Literal[
    "foundation_final_screen_state",
    "interaction_final_screen_state",
]

FinalScreenStateMode = Literal[
    "assembled_foundation_final_screen_state",
    "assembled_interaction_final_screen_state",
]

ALL_FINAL_SCREEN_STATE_STATES: tuple[FinalScreenStateState, ...] = (
    "final_screen_state_ready",
)

ALL_FINAL_SCREEN_STATE_CLASSES: tuple[FinalScreenStateClass, ...] = (
    "foundation_final_screen_state",
    "interaction_final_screen_state",
)

ALL_FINAL_SCREEN_STATE_MODES: tuple[FinalScreenStateMode, ...] = (
    "assembled_foundation_final_screen_state",
    "assembled_interaction_final_screen_state",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class FinalScreenStateEntry:
    """Canonical final screen state entry."""

    final_screen_state_id: str
    display_target_id: str
    workspace_id: str
    final_screen_state_state: FinalScreenStateState
    final_screen_state_class: FinalScreenStateClass
    final_screen_state_mode: FinalScreenStateMode
    final_visible_screen_state_ready: bool
    presentation_bundle_runtime_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.final_screen_state_id, "final_screen_state_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.final_screen_state_state not in ALL_FINAL_SCREEN_STATE_STATES:
            raise ValueError(
                "final_screen_state_state must be one of "
                f"{ALL_FINAL_SCREEN_STATE_STATES}, got {self.final_screen_state_state!r}."
            )

        if self.final_screen_state_class not in ALL_FINAL_SCREEN_STATE_CLASSES:
            raise ValueError(
                "final_screen_state_class must be one of "
                f"{ALL_FINAL_SCREEN_STATE_CLASSES}, got {self.final_screen_state_class!r}."
            )

        if self.final_screen_state_mode not in ALL_FINAL_SCREEN_STATE_MODES:
            raise ValueError(
                "final_screen_state_mode must be one of "
                f"{ALL_FINAL_SCREEN_STATE_MODES}, got {self.final_screen_state_mode!r}."
            )

        if not self.final_visible_screen_state_ready:
            raise ValueError(
                "final_visible_screen_state_ready must remain true for canonical final screen state entries."
            )

        if not self.presentation_bundle_runtime_ready:
            raise ValueError(
                "presentation_bundle_runtime_ready must remain true for canonical final screen state entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical final screen state entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical final screen state entries."
            )

        if (
            self.final_screen_state_class == "foundation_final_screen_state"
            and self.final_screen_state_mode
            != "assembled_foundation_final_screen_state"
        ):
            raise ValueError(
                "foundation_final_screen_state must use assembled_foundation_final_screen_state."
            )

        if (
            self.final_screen_state_class == "interaction_final_screen_state"
            and self.final_screen_state_mode
            != "assembled_interaction_final_screen_state"
        ):
            raise ValueError(
                "interaction_final_screen_state must use assembled_interaction_final_screen_state."
            )


@dataclass(frozen=True, slots=True)
class FinalScreenStateContract:
    """Canonical final screen state contract."""

    contract_id: str
    total_entries: int
    foundation_final_entries: int
    interaction_final_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[FinalScreenStateEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_final_entries != sum(
            1
            for entry in self.entries
            if entry.final_screen_state_class == "foundation_final_screen_state"
        ):
            raise ValueError(
                "foundation_final_entries must match foundation_final_screen_state count."
            )

        if self.interaction_final_entries != sum(
            1
            for entry in self.entries
            if entry.final_screen_state_class == "interaction_final_screen_state"
        ):
            raise ValueError(
                "interaction_final_entries must match interaction_final_screen_state count."
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
