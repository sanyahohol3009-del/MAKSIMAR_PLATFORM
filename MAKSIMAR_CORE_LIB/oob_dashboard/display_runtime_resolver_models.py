from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DisplayRuntimeResolverEntry:
    """Canonical display runtime resolver entry."""

    panel_id: str
    view_id: str
    display_target_id: str
    resolved_display_role: str
    resolved_display_zone: str
    fallback_display_target_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate resolver entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.view_id.strip():
            raise ValueError("view_id must not be empty")

        if not self.display_target_id.strip():
            raise ValueError("display_target_id must not be empty")

        if not self.resolved_display_role.strip():
            raise ValueError("resolved_display_role must not be empty")

        if not self.resolved_display_zone.strip():
            raise ValueError("resolved_display_zone must not be empty")

        if not self.fallback_display_target_id.strip():
            raise ValueError("fallback_display_target_id must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class DisplayRuntimeResolverContract:
    """Canonical ordered display runtime resolver contract."""

    entries: tuple[DisplayRuntimeResolverEntry, ...]

    def __post_init__(self) -> None:
        """Validate resolver contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_panel_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_panel_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_panel_ids.add(entry.panel_id)
