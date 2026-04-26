from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardReadRow:
    """Read-only row describing the assembled main operator dashboard."""

    dashboard_id: str
    dashboard_role: str
    primary_workspace_id: str
    secondary_workspace_ids: tuple[str, ...]
    total_workspace_count: int
    total_panel_count: int
    read_only_foundation_reuse: bool
    supports_multimonitor_layout: bool
    supports_voice_gesture_addressing: bool
    description: str

    def __post_init__(self) -> None:
        """Validate read-row invariants."""
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")

        if not self.dashboard_role.strip():
            raise ValueError("dashboard_role must not be empty")

        if not self.primary_workspace_id.strip():
            raise ValueError("primary_workspace_id must not be empty")

        if self.total_workspace_count < 1:
            raise ValueError("total_workspace_count must be >= 1")

        if self.total_panel_count < 1:
            raise ValueError("total_panel_count must be >= 1")

        if self.read_only_foundation_reuse is not True:
            raise ValueError("read_only_foundation_reuse must be True")

        if self.supports_multimonitor_layout is not True:
            raise ValueError("supports_multimonitor_layout must be True")

        if self.supports_voice_gesture_addressing is not True:
            raise ValueError("supports_voice_gesture_addressing must be True")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardReadModelContract:
    """Canonical read-model contract for the main operator dashboard."""

    rows: tuple[MainOperatorDashboardReadRow, ...]

    def __post_init__(self) -> None:
        """Validate read-model contract invariants."""
        if not self.rows:
            raise ValueError("rows must not be empty")

        seen_dashboard_ids: set[str] = set()
        for row in self.rows:
            if row.dashboard_id in seen_dashboard_ids:
                raise ValueError(f"duplicate dashboard_id detected: {row.dashboard_id}")
            seen_dashboard_ids.add(row.dashboard_id)
