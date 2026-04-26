from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PreviewSurfaceState = Literal[
    "preview_surface_ready",
]

PreviewSurfaceClass = Literal[
    "foundation_preview_surface",
    "interaction_preview_surface",
]

PreviewGenerationMode = Literal[
    "panel_preview_generation",
    "fixture_preview_generation",
]

ALL_PREVIEW_SURFACE_STATES: tuple[PreviewSurfaceState, ...] = (
    "preview_surface_ready",
)

ALL_PREVIEW_SURFACE_CLASSES: tuple[PreviewSurfaceClass, ...] = (
    "foundation_preview_surface",
    "interaction_preview_surface",
)

ALL_PREVIEW_GENERATION_MODES: tuple[PreviewGenerationMode, ...] = (
    "panel_preview_generation",
    "fixture_preview_generation",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PreviewSurfaceEntry:
    """Canonical preview surface entry."""

    preview_surface_id: str
    panel_id: str
    workspace_id: str
    preview_surface_state: PreviewSurfaceState
    preview_surface_class: PreviewSurfaceClass
    preview_generation_mode: PreviewGenerationMode
    visible_in_navigation: bool
    visible_in_main_dashboard: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.preview_surface_id, "preview_surface_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.preview_surface_state not in ALL_PREVIEW_SURFACE_STATES:
            raise ValueError(
                "preview_surface_state must be one of "
                f"{ALL_PREVIEW_SURFACE_STATES}, got {self.preview_surface_state!r}."
            )

        if self.preview_surface_class not in ALL_PREVIEW_SURFACE_CLASSES:
            raise ValueError(
                "preview_surface_class must be one of "
                f"{ALL_PREVIEW_SURFACE_CLASSES}, got {self.preview_surface_class!r}."
            )

        if self.preview_generation_mode not in ALL_PREVIEW_GENERATION_MODES:
            raise ValueError(
                "preview_generation_mode must be one of "
                f"{ALL_PREVIEW_GENERATION_MODES}, got {self.preview_generation_mode!r}."
            )

        if not self.visible_in_navigation:
            raise ValueError(
                "visible_in_navigation must remain true for canonical preview surfaces."
            )

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical preview surfaces."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical preview surfaces."
            )


@dataclass(frozen=True, slots=True)
class PreviewSurfaceContract:
    """Canonical preview surface contract."""

    contract_id: str
    total_entries: int
    foundation_preview_entries: int
    interaction_preview_entries: int
    panel_preview_generation_entries: int
    fixture_preview_generation_entries: int
    operator_visible_entries: int
    entries: tuple[PreviewSurfaceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_preview_entries != sum(
            1
            for entry in self.entries
            if entry.preview_surface_class == "foundation_preview_surface"
        ):
            raise ValueError(
                "foundation_preview_entries must match foundation_preview_surface count."
            )

        if self.interaction_preview_entries != sum(
            1
            for entry in self.entries
            if entry.preview_surface_class == "interaction_preview_surface"
        ):
            raise ValueError(
                "interaction_preview_entries must match interaction_preview_surface count."
            )

        if self.panel_preview_generation_entries != sum(
            1
            for entry in self.entries
            if entry.preview_generation_mode == "panel_preview_generation"
        ):
            raise ValueError(
                "panel_preview_generation_entries must match panel_preview_generation count."
            )

        if self.fixture_preview_generation_entries != sum(
            1
            for entry in self.entries
            if entry.preview_generation_mode == "fixture_preview_generation"
        ):
            raise ValueError(
                "fixture_preview_generation_entries must match fixture_preview_generation count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
