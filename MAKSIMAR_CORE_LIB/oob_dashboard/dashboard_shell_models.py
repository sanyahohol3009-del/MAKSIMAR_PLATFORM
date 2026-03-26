from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardShellContract:
    """Final shell contract for OOB dashboard."""

    shell_id: str
    total_panels: int
    total_displays: int
    total_feedback_items: int
    consistency_status: str
    active_panel_id: str
