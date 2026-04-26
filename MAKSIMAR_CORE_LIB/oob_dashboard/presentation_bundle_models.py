from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PresentationBundleRuntimeState = Literal[
    "presentation_bundle_runtime_ready",
]

PresentationBundleRuntimeClass = Literal[
    "foundation_presentation_runtime",
    "interaction_presentation_runtime",
]

PresentationBundleRuntimeMode = Literal[
    "assembled_foundation_presentation_runtime",
    "assembled_interaction_presentation_runtime",
]

ALL_PRESENTATION_BUNDLE_RUNTIME_STATES: tuple[PresentationBundleRuntimeState, ...] = (
    "presentation_bundle_runtime_ready",
)

ALL_PRESENTATION_BUNDLE_RUNTIME_CLASSES: tuple[PresentationBundleRuntimeClass, ...] = (
    "foundation_presentation_runtime",
    "interaction_presentation_runtime",
)

ALL_PRESENTATION_BUNDLE_RUNTIME_MODES: tuple[PresentationBundleRuntimeMode, ...] = (
    "assembled_foundation_presentation_runtime",
    "assembled_interaction_presentation_runtime",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PresentationBundleRuntimeEntry:
    """Canonical presentation-bundle runtime entry."""

    presentation_bundle_runtime_id: str
    display_target_id: str
    workspace_id: str
    presentation_bundle_runtime_state: PresentationBundleRuntimeState
    presentation_bundle_runtime_class: PresentationBundleRuntimeClass
    presentation_bundle_runtime_mode: PresentationBundleRuntimeMode
    visible_state_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.presentation_bundle_runtime_id,
            "presentation_bundle_runtime_id",
        )
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.presentation_bundle_runtime_state not in ALL_PRESENTATION_BUNDLE_RUNTIME_STATES:
            raise ValueError(
                "presentation_bundle_runtime_state must be one of "
                f"{ALL_PRESENTATION_BUNDLE_RUNTIME_STATES}, got {self.presentation_bundle_runtime_state!r}."
            )

        if self.presentation_bundle_runtime_class not in ALL_PRESENTATION_BUNDLE_RUNTIME_CLASSES:
            raise ValueError(
                "presentation_bundle_runtime_class must be one of "
                f"{ALL_PRESENTATION_BUNDLE_RUNTIME_CLASSES}, got {self.presentation_bundle_runtime_class!r}."
            )

        if self.presentation_bundle_runtime_mode not in ALL_PRESENTATION_BUNDLE_RUNTIME_MODES:
            raise ValueError(
                "presentation_bundle_runtime_mode must be one of "
                f"{ALL_PRESENTATION_BUNDLE_RUNTIME_MODES}, got {self.presentation_bundle_runtime_mode!r}."
            )

        if not self.visible_state_ready:
            raise ValueError(
                "visible_state_ready must remain true for canonical presentation-bundle runtime entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical presentation-bundle runtime entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical presentation-bundle runtime entries."
            )

        if (
            self.presentation_bundle_runtime_class == "foundation_presentation_runtime"
            and self.presentation_bundle_runtime_mode
            != "assembled_foundation_presentation_runtime"
        ):
            raise ValueError(
                "foundation_presentation_runtime must use assembled_foundation_presentation_runtime."
            )

        if (
            self.presentation_bundle_runtime_class == "interaction_presentation_runtime"
            and self.presentation_bundle_runtime_mode
            != "assembled_interaction_presentation_runtime"
        ):
            raise ValueError(
                "interaction_presentation_runtime must use assembled_interaction_presentation_runtime."
            )


@dataclass(frozen=True, slots=True)
class PresentationBundleRuntimeContract:
    """Canonical presentation-bundle runtime contract."""

    contract_id: str
    total_entries: int
    foundation_runtime_entries: int
    interaction_runtime_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[PresentationBundleRuntimeEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_runtime_entries != sum(
            1
            for entry in self.entries
            if entry.presentation_bundle_runtime_class == "foundation_presentation_runtime"
        ):
            raise ValueError(
                "foundation_runtime_entries must match foundation_presentation_runtime count."
            )

        if self.interaction_runtime_entries != sum(
            1
            for entry in self.entries
            if entry.presentation_bundle_runtime_class == "interaction_presentation_runtime"
        ):
            raise ValueError(
                "interaction_runtime_entries must match interaction_presentation_runtime count."
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
