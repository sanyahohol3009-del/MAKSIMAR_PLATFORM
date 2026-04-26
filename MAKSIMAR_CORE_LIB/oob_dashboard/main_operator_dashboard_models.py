from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardEntry:
    """Canonical main-operator dashboard entry."""

    dashboard_id: str
    dashboard_role: str
    primary_workspace_id: str
    secondary_workspace_ids: tuple[str, ...]
    read_only_foundation_reuse: bool
    creates_second_root: bool
    description: str

    def __post_init__(self) -> None:
        """Validate main-operator dashboard entry invariants."""
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")

        if not self.dashboard_role.strip():
            raise ValueError("dashboard_role must not be empty")

        if not self.primary_workspace_id.strip():
            raise ValueError("primary_workspace_id must not be empty")

        if self.read_only_foundation_reuse is not True:
            raise ValueError("read_only_foundation_reuse must be True")

        if self.creates_second_root is not False:
            raise ValueError("creates_second_root must be False")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardContract:
    """Canonical main-operator dashboard contract."""

    entries: tuple[MainOperatorDashboardEntry, ...]

    def __post_init__(self) -> None:
        """Validate dashboard contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_dashboard_ids: set[str] = set()
        for entry in self.entries:
            if entry.dashboard_id in seen_dashboard_ids:
                raise ValueError(
                    f"duplicate dashboard_id detected: {entry.dashboard_id}"
                )
            seen_dashboard_ids.add(entry.dashboard_id)
