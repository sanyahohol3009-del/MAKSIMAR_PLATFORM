from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract import (
    build_system_status_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


StatusBarSeverity = Literal[
    "normal",
    "warning",
    "critical",
]

StatusBarMode = Literal[
    "foundation_summary",
    "operator_summary",
]


@dataclass(frozen=True, slots=True)
class VisualStatusBarEntry:
    """Canonical visual status bar entry for top HUD strip."""

    status_bar_id: str
    panel_id: str
    renderer_surface_id: str
    severity: StatusBarSeverity
    mode: StatusBarMode
    total_runtime_surfaces: int
    active_runtime_surfaces: int
    warning_runtime_surfaces: int
    visible: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualStatusBarContract:
    """Canonical visual status bar contract for top HUD strip."""

    contract_id: str
    total_entries: int
    normal_entries: int
    warning_entries: int
    critical_entries: int
    visible_entries: int
    read_only_entries: int
    entries: tuple[VisualStatusBarEntry, ...]


def _severity_for_system_status(
    *,
    total_runtime_surfaces: int,
    active_runtime_surfaces: int,
    warning_runtime_surfaces: int,
) -> StatusBarSeverity:
    """Resolve status-bar severity from system summary counters."""
    if active_runtime_surfaces == total_runtime_surfaces and warning_runtime_surfaces == 0:
        return "normal"
    if active_runtime_surfaces > 0:
        return "warning"
    return "critical"


def build_visual_status_bar_contract() -> VisualStatusBarContract:
    """Build canonical visual status bar contract."""
    system_status_contract = build_system_status_panel_content_contract()
    render_surface_contract = build_visual_render_surface_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id
    system_status_entry = system_status_contract.entries[0]

    total_runtime_surfaces = 4
    active_runtime_surfaces = 4
    warning_runtime_surfaces = 0

    entries = (
        VisualStatusBarEntry(
            status_bar_id="visual_status_bar_001",
            panel_id=system_status_entry.panel_id,
            renderer_surface_id=renderer_surface_id,
            severity=_severity_for_system_status(
                total_runtime_surfaces=total_runtime_surfaces,
                active_runtime_surfaces=active_runtime_surfaces,
                warning_runtime_surfaces=warning_runtime_surfaces,
            ),
            mode="foundation_summary",
            total_runtime_surfaces=total_runtime_surfaces,
            active_runtime_surfaces=active_runtime_surfaces,
            warning_runtime_surfaces=warning_runtime_surfaces,
            visible=True,
            read_only=True,
            description=(
                "Canonical visual status bar entry for top HUD summary."
            ),
        ),
    )

    return VisualStatusBarContract(
        contract_id="visual_status_bar_contract_001",
        total_entries=len(entries),
        normal_entries=sum(1 for entry in entries if entry.severity == "normal"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        visible_entries=sum(1 for entry in entries if entry.visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
