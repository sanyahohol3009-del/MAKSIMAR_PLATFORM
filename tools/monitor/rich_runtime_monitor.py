from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


PROJECT_ROOT = Path.home() / "MAKSIMAR_PLATFORM"
RUNTIME_STATE_DIR = PROJECT_ROOT / "MAKSIMAR_SERVER" / "RUNTIME" / "state"
LOGS_DIR = PROJECT_ROOT / "MAKSIMAR_SERVER" / "logs"


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
    """Return last lines from a log file if it exists."""
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return lines[-max_lines:]
    except OSError:
        return []


def build_status_cards() -> list[MonitorStatusCard]:
    """Build read-only monitor cards from canonical file paths."""
    preflight = _read_json_if_exists(RUNTIME_STATE_DIR / "preflight_snapshot.json")
    incident = _read_json_if_exists(RUNTIME_STATE_DIR / "last_incident.json")
    degraded = _read_json_if_exists(RUNTIME_STATE_DIR / "degraded_flags.json")

    return [
        MonitorStatusCard(
            title="Preflight",
            value="present" if preflight else "missing",
            detail="canonical startup snapshot",
        ),
        MonitorStatusCard(
            title="Incident",
            value="present" if incident else "none",
            detail="last incident snapshot",
        ),
        MonitorStatusCard(
            title="Degraded",
            value="active" if degraded else "clear",
            detail="degraded flag state",
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
