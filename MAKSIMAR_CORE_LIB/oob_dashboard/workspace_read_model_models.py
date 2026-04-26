from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkspaceReadRow:
    """Read-only row for workspace inspection."""

    workspace_id: str
    workspace_role: str
    primary_display_target_id: str
    panel_count: int
    panel_ids: tuple[str, ...]
    description: str

    def __post_init__(self) -> None:
        """Validate workspace read row invariants."""
        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")

        if not self.workspace_role.strip():
            raise ValueError("workspace_role must not be empty")

        if not self.primary_display_target_id.strip():
            raise ValueError("primary_display_target_id must not be empty")

        if self.panel_count < 0:
            raise ValueError("panel_count must be >= 0")

        if self.panel_count != len(self.panel_ids):
            raise ValueError("panel_count must match len(panel_ids)")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class WorkspaceReadModelContract:
    """Canonical workspace read-model contract."""

    rows: tuple[WorkspaceReadRow, ...]

    def __post_init__(self) -> None:
        """Validate workspace read-model contract invariants."""
        if not self.rows:
            raise ValueError("rows must not be empty")

        seen_workspace_ids: set[str] = set()
        for row in self.rows:
            if row.workspace_id in seen_workspace_ids:
                raise ValueError(
                    f"duplicate workspace_id detected: {row.workspace_id}"
                )
            seen_workspace_ids.add(row.workspace_id)
