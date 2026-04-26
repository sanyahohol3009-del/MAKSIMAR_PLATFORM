from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LayoutCompositionEntry:
    """Canonical layout composition entry."""

    workspace_id: str
    panel_id: str
    layout_slot_id: str
    layout_zone: str
    slot_order: int
    description: str

    def __post_init__(self) -> None:
        """Validate layout composition entry invariants."""
        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")

        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.layout_slot_id.strip():
            raise ValueError("layout_slot_id must not be empty")

        if not self.layout_zone.strip():
            raise ValueError("layout_zone must not be empty")

        if self.slot_order < 0:
            raise ValueError("slot_order must be >= 0")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class LayoutCompositionContract:
    """Canonical ordered layout composition contract."""

    entries: tuple[LayoutCompositionEntry, ...]

    def __post_init__(self) -> None:
        """Validate layout composition contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")
