from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_diagnostics_correlation_view import (
    build_foundation_diagnostics_correlation_view,
)


LogsPanelStatus = Literal[
    "diagnostics_visible",
    "no_diagnostics_visible",
]


@dataclass(frozen=True, slots=True)
class LogsPanelContentEntry:
    """Canonical content entry for the logs panel."""

    panel_id: str
    total_log_related_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    source_file_visible_entries: int
    failure_visible_entries: int
    logs_panel_status: LogsPanelStatus
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class LogsPanelContentContract:
    """Canonical content contract for the logs panel."""

    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: tuple[LogsPanelContentEntry, ...]


def build_logs_panel_content_contract() -> LogsPanelContentContract:
    """Build canonical content contract for the logs panel."""
    diagnostics_view = build_foundation_diagnostics_correlation_view()

    entries = (
        LogsPanelContentEntry(
            panel_id="panel_logs_001",
            total_log_related_entries=len(diagnostics_view.entries),
            critical_entries=sum(
                1 for entry in diagnostics_view.entries if entry.severity == "critical"
            ),
            warning_entries=sum(
                1 for entry in diagnostics_view.entries if entry.severity == "warning"
            ),
            info_entries=sum(
                1 for entry in diagnostics_view.entries if entry.severity == "info"
            ),
            source_file_visible_entries=sum(
                1
                for entry in diagnostics_view.entries
                if entry.suspected_source_file != "unknown"
            ),
            failure_visible_entries=sum(
                1 for entry in diagnostics_view.entries if entry.failure_visible
            ),
            logs_panel_status=(
                "diagnostics_visible"
                if len(diagnostics_view.entries) > 0
                else "no_diagnostics_visible"
            ),
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            read_only=True,
            description=(
                "Canonical logs panel content contract built from "
                "foundation diagnostics correlation view."
            ),
        ),
    )

    return LogsPanelContentContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for entry in entries if entry.visible_in_oob_dashboard
        ),
        entries=entries,
    )
