from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingEntry:
    """Canonical operator-to-workspace binding entry."""

    dashboard_id: str
    workspace_id: str
    binding_role: str
    workspace_order: int
    is_primary_workspace: bool
    read_only_binding: bool
    description: str

    def __post_init__(self) -> None:
        """Validate binding entry invariants."""
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")

        if not self.workspace_id.strip():
            raise ValueError("workspace_id must not be empty")

        if not self.binding_role.strip():
            raise ValueError("binding_role must not be empty")

        if self.workspace_order < 0:
            raise ValueError("workspace_order must be >= 0")

        if self.read_only_binding is not True:
            raise ValueError("read_only_binding must be True")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingContract:
    """Canonical operator-workspace binding contract."""

    entries: tuple[OperatorWorkspaceBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate binding contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_pairs: set[tuple[str, str]] = set()
        primary_count = 0

        for entry in self.entries:
            key = (entry.dashboard_id, entry.workspace_id)
            if key in seen_pairs:
                raise ValueError(
                    "duplicate dashboard_id/workspace_id detected: "
                    f"{entry.dashboard_id}/{entry.workspace_id}"
                )
            seen_pairs.add(key)

            if entry.is_primary_workspace:
                primary_count += 1

        if primary_count != 1:
            raise ValueError("exactly one primary workspace must be defined")
