from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_content_contract import (
    build_logs_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)

TickerSeverity = Literal[
    "normal",
    "warning",
    "critical",
]

TickerMode = Literal[
    "log_stream",
    "incident_stream",
]


@dataclass(frozen=True, slots=True)
class VisualBottomTickerEntry:
    """Canonical visual bottom ticker entry for HUD bottom strip."""

    ticker_id: str
    panel_id: str
    renderer_surface_id: str
    severity: TickerSeverity
    mode: TickerMode
    total_log_sources: int
    active_log_sources: int
    highlighted_log_sources: int
    visible: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualBottomTickerContract:
    """Canonical visual bottom ticker contract for HUD bottom strip."""

    contract_id: str
    total_entries: int
    normal_entries: int
    warning_entries: int
    critical_entries: int
    visible_entries: int
    read_only_entries: int
    entries: tuple[VisualBottomTickerEntry, ...]


def _severity_for_ticker(
    *,
    total_log_sources: int,
    active_log_sources: int,
    highlighted_log_sources: int,
) -> TickerSeverity:
    """Resolve ticker severity from log source counters."""
    if active_log_sources == total_log_sources and highlighted_log_sources == 0:
        return "normal"
    if active_log_sources > 0:
        return "warning"
    return "critical"


def build_visual_bottom_ticker_contract() -> VisualBottomTickerContract:
    """Build canonical visual bottom ticker contract."""
    logs_contract = build_logs_panel_content_contract()
    render_surface_contract = build_visual_render_surface_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id
    logs_entry = logs_contract.entries[0]

    total_log_sources = logs_entry.total_log_related_entries
    highlighted_log_sources = (
        logs_entry.critical_entries
        + logs_entry.warning_entries
        + logs_entry.failure_visible_entries
    )
    active_log_sources = max(total_log_sources - highlighted_log_sources, 0)

    entries = (
        VisualBottomTickerEntry(
            ticker_id="visual_bottom_ticker_001",
            panel_id=logs_entry.panel_id,
            renderer_surface_id=renderer_surface_id,
            severity=_severity_for_ticker(
                total_log_sources=total_log_sources,
                active_log_sources=active_log_sources,
                highlighted_log_sources=highlighted_log_sources,
            ),
            mode="log_stream",
            total_log_sources=total_log_sources,
            active_log_sources=active_log_sources,
            highlighted_log_sources=highlighted_log_sources,
            visible=True,
            read_only=True,
            description=(
                "Canonical visual bottom ticker entry derived from "
                "logs panel content."
            ),
        ),
    )

    return VisualBottomTickerContract(
        contract_id="visual_bottom_ticker_contract_001",
        total_entries=len(entries),
        normal_entries=sum(1 for entry in entries if entry.severity == "normal"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        visible_entries=sum(1 for entry in entries if entry.visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
