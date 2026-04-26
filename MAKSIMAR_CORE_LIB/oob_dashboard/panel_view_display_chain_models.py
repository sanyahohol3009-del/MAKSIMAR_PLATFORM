from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PanelViewDisplayChainEntry:
    """Canonical panel → view → display chain entry."""

    panel_id: str
    view_id: str
    display_target_id: str
    display_role: str
    display_zone: str
    is_default_chain: bool
    description: str

    def __post_init__(self) -> None:
        """Validate chain entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.view_id.strip():
            raise ValueError("view_id must not be empty")

        if not self.display_target_id.strip():
            raise ValueError("display_target_id must not be empty")

        if not self.display_role.strip():
            raise ValueError("display_role must not be empty")

        if not self.display_zone.strip():
            raise ValueError("display_zone must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelViewDisplayChainContract:
    """Canonical ordered panel → view → display chain contract."""

    entries: tuple[PanelViewDisplayChainEntry, ...]

    def __post_init__(self) -> None:
        """Validate chain contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_panel_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_panel_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_panel_ids.add(entry.panel_id)
