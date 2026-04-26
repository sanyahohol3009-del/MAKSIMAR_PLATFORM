from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PanelBindingEntry:
    """Canonical panel-to-display binding entry."""

    panel_id: str
    display_target_id: str
    binding_reason: str
    is_default_target: bool
    eligible_for_main_dashboard: bool
    eligible_for_oob_dashboard: bool
    description: str

    def __post_init__(self) -> None:
        """Validate panel-binding entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.display_target_id.strip():
            raise ValueError("display_target_id must not be empty")

        if not self.binding_reason.strip():
            raise ValueError("binding_reason must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelBindingContract:
    """Canonical ordered panel-binding contract."""

    entries: tuple[PanelBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate panel-binding contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_panel_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_panel_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_panel_ids.add(entry.panel_id)
