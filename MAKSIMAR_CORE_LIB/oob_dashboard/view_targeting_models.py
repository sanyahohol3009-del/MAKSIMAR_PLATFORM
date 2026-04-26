from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ViewTargetingEntry:
    """Canonical panel-to-view targeting entry."""

    panel_id: str
    view_id: str
    view_target_kind: str
    view_scope: str
    description: str

    def __post_init__(self) -> None:
        """Validate view-targeting entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.view_id.strip():
            raise ValueError("view_id must not be empty")

        if not self.view_target_kind.strip():
            raise ValueError("view_target_kind must not be empty")

        if not self.view_scope.strip():
            raise ValueError("view_scope must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class ViewTargetingContract:
    """Canonical ordered view-targeting contract."""

    entries: tuple[ViewTargetingEntry, ...]

    def __post_init__(self) -> None:
        """Validate view-targeting contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_panel_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_panel_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_panel_ids.add(entry.panel_id)
