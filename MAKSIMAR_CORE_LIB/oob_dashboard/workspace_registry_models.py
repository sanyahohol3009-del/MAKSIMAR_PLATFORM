from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkspaceRegistryEntry:
    """Canonical workspace registry entry."""

    workspace_id: str
    workspace_role: str
    primary_display_target_id: str
    included_panel_ids: tuple[str, ...]
    description: str

    def __post_init__(self) -> None:
        """Validate workspace registry entry invariants."""
        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")

        if not self.workspace_role.strip():
            raise ValueError("workspace_role must not be empty")

        if not self.primary_display_target_id.strip():
            raise ValueError("primary_display_target_id must not be empty")

        if not self.included_panel_ids:
            raise ValueError("included_panel_ids must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class WorkspaceRegistryContract:
    """Canonical ordered workspace registry contract."""

    entries: tuple[WorkspaceRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate workspace registry contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_workspace_ids: set[str] = set()
        for entry in self.entries:
            if entry.workspace_id in seen_workspace_ids:
                raise ValueError(
                    f"duplicate workspace_id detected: {entry.workspace_id}"
                )
            seen_workspace_ids.add(entry.workspace_id)
