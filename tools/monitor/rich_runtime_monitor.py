from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


from CORE_ROOT.runtime_paths import ROOT as PROJECT_ROOT, RUNTIME_STATE_DIR, LOGS_DIR


@dataclass(frozen=True, slots=True)
class MonitorStatusCard:
    """Simple read-only status card for terminal monitor output."""

    title: str
    value: str
    detail: str


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    """Read JSON file if it exists, otherwise return empty dict."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _tail_lines(path: Path, max_lines: int = 5) -> list[str]:
    """Reuse the existing bounded OOB log-tail reader."""
    from tools.monitor.oob_foundation_monitor import tail_log
    return tail_log(path, max_lines)


def build_status_cards() -> list[MonitorStatusCard]:
    """Build read-only monitor cards from canonical file paths."""
    from CORE_ROOT import runtime_paths
    preflight = _read_json_if_exists(runtime_paths.PREFLIGHT_RESULT_FILE)
    incident = _read_json_if_exists(runtime_paths.INCIDENT_SNAPSHOT_FILE)
    state_present = runtime_paths.RUNTIME_STATE_DIR.is_dir()
    degraded_present = runtime_paths.DEGRADED_MODE_FILE.exists()
    return [
        MonitorStatusCard(
            title="Preflight",
            value=("passed" if preflight.get("ok") is True else "failed" if preflight.get("ok") is False else "unknown") if preflight else "missing",
            detail="retained startup observation; not current runtime readiness",
        ),
        MonitorStatusCard(
            title="Incident",
            value="present" if incident else "unavailable",
            detail="retained last incident snapshot; absence is not incident-free proof",
        ),
        MonitorStatusCard(
            title="Degraded",
            value="active" if degraded_present else "flag_absent" if state_present else "unknown",
            detail="canonical degraded flag presence; not whole-runtime health",
        ),
    ]


def build_status_table() -> Table:
    """Build a read-only status summary table."""
    table = Table(title="MAKSIMAR Read-Only Monitor")
    table.add_column("Item")
    table.add_column("State")
    table.add_column("Detail")

    for card in build_status_cards():
        table.add_row(card.title, card.value, card.detail)

    return table


def build_logs_panel() -> Panel:
    """Build a panel showing recent log lines."""
    log_candidates = [
        LOGS_DIR / "guard.log",
        LOGS_DIR / "core_guard.log",
        LOGS_DIR / "kernel_guard.log",
    ]

    lines: list[str] = []
    for path in log_candidates:
        tailed = _tail_lines(path, max_lines=2)
        if tailed:
            lines.append(f"[{path.name}]")
            lines.extend(tailed)

    if not lines:
        lines = ["No recent logs found in canonical log paths."]

    body = Text("\n".join(lines))
    return Panel(body, title="Recent Logs", border_style="cyan")


def render_monitor(console: Console | None = None) -> None:
    """Render read-only monitor output to terminal."""
    local_console = console or Console()
    local_console.print(build_status_table())
    local_console.print(build_logs_panel())


if __name__ == "__main__":
    render_monitor()
