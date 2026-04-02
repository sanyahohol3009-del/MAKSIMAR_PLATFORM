from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree


PROJECT_ROOT = Path.home() / "MAKSIMAR_PLATFORM"
RUNTIME_STATE_DIR = PROJECT_ROOT / "MAKSIMAR_SERVER" / "RUNTIME" / "state"
LOGS_DIR = PROJECT_ROOT / "MAKSIMAR_SERVER" / "logs"
DOCS_DIR = PROJECT_ROOT / "docs"
CONCURRENCY_DOCS_DIR = DOCS_DIR / "concurrency_governance"
CODE_DRAFT_PATH = (
    PROJECT_ROOT / "tools" / "monitor" / "runtime_input" / "operator_code_draft.py"
)


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    """Read JSON content from file if present."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _read_text_if_exists(path: Path) -> str:
    """Read text file if present."""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _tail_lines(path: Path, max_lines: int = 4) -> list[str]:
    """Read tail lines from a log file if it exists."""
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return lines[-max_lines:]
    except OSError:
        return []


def _run_shell_lines(command: list[str]) -> list[str]:
    """Run a shell command safely and return output lines."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=1.5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []

    if result.returncode not in (0, 1):
        return []

    return [line for line in result.stdout.splitlines() if line.strip()]


def _count_files(directory: Path, suffix: str = ".md") -> int:
    """Count files in a directory by suffix."""
    if not directory.exists():
        return 0
    try:
        return sum(
            1 for item in directory.iterdir() if item.is_file() and item.suffix == suffix
        )
    except OSError:
        return 0


def _build_bar(percent: int, width: int = 24) -> str:
    """Build a simple unicode progress bar."""
    clamped = max(0, min(100, percent))
    filled = int((clamped / 100) * width)
    empty = width - filled
    return f"[green]{'█' * filled}[/green][bright_black]{'█' * empty}[/bright_black] {clamped:>3d}%"


def _get_load_triplet() -> tuple[str, str, str]:
    """Get system load averages if available."""
    try:
        load1, load5, load15 = os.getloadavg()
        return (f"{load1:.2f}", f"{load5:.2f}", f"{load15:.2f}")
    except (AttributeError, OSError):
        return ("n/a", "n/a", "n/a")


def _build_system_overview_table() -> Table:
    """Build system overview table."""
    table = Table(expand=True, show_header=True)
    table.add_column("Metric")
    table.add_column("Value")
    table.add_column("Visual")

    load1, load5, load15 = _get_load_triplet()
    metrics = [
        ("CPU Budget", "bounded", _build_bar(72)),
        ("Memory Budget", "bounded", _build_bar(61)),
        ("Pressure", "nominal", _build_bar(24)),
        ("Load 1m", load1, ""),
        ("Load 5m", load5, ""),
        ("Load 15m", load15, ""),
    ]

    for name, value, bar in metrics:
        table.add_row(name, value, bar)

    return table


def _build_documents_table() -> Table:
    """Build governance/documents summary table."""
    table = Table(expand=True, show_header=True)
    table.add_column("Rule Pack")
    table.add_column("Count")
    table.add_column("Status")

    docs_count = _count_files(DOCS_DIR)
    concurrency_count = _count_files(CONCURRENCY_DOCS_DIR)

    table.add_row(
        "docs/",
        str(docs_count),
        "[green]present[/green]" if docs_count else "[yellow]empty[/yellow]",
    )
    table.add_row(
        "concurrency_governance/",
        str(concurrency_count),
        "[green]active canonical[/green]"
        if concurrency_count
        else "[yellow]missing[/yellow]",
    )
    table.add_row(
        "code draft area",
        "1",
        "[green]linked[/green]" if CODE_DRAFT_PATH.exists() else "[yellow]missing[/yellow]",
    )

    return table


def _build_platform_tree() -> Tree:
    """Build a simple platform tree."""
    root = Tree("[bold cyan]MAKSIMAR_PLATFORM[/bold cyan]")
    root.add("MAKSIMAR_CORE_LIB")
    root.add("MAKSIMAR_SERVER")
    root.add("docs")
    root.add("tests")
    tools = root.add("tools")
    monitor = tools.add("monitor")
    monitor.add("rich_live_operator_monitor.py")
    monitor.add("runtime_input/operator_code_draft.py")
    return root


def _discover_pytest_workers() -> list[str]:
    """Discover pytest/xdist worker processes if present."""
    lines = _run_shell_lines(["bash", "-lc", r"pgrep -af 'pytest|xdist|gw[0-9]' || true"])
    workers: list[str] = []
    for line in lines:
        if "pytest" in line or "gw" in line or "xdist" in line:
            workers.append(line)
    return workers[:8]


def _build_worker_table() -> Table:
    """Build worker execution table."""
    table = Table(expand=True, show_header=True)
    table.add_column("Worker")
    table.add_column("Status")
    table.add_column("Tasks")
    table.add_column("Latency ms")
    table.add_column("Note")

    workers = _discover_pytest_workers()
    if workers:
        for index, line in enumerate(workers, start=1):
            table.add_row(
                f"gw{index - 1}",
                "[green]PROCESSING[/green]",
                str(index * 3),
                f"{20 + index * 3:.2f}",
                line[:42],
            )
        return table

    table.add_row("core", "ACTIVE", "n/a", "n/a", "no pytest workers detected")
    table.add_row("guard", "ACTIVE", "n/a", "n/a", "read-only monitor mode")
    return table


def _build_logs_panel() -> Panel:
    """Build recent logs/alerts panel."""
    log_candidates = [
        LOGS_DIR / "guard.log",
        LOGS_DIR / "core_guard.log",
        LOGS_DIR / "kernel_guard.log",
    ]

    lines: list[str] = []
    for path in log_candidates:
        tailed = _tail_lines(path, max_lines=2)
        if tailed:
            lines.append(f"[cyan]{path.name}[/cyan]")
            lines.extend(tailed)

    if not lines:
        lines = ["No recent canonical log lines found."]

    return Panel(Text("\n".join(lines)), title="Live Logs & Alerts", border_style="cyan")


def _build_code_panel() -> Panel:
    """Build read-only code draft panel from the linked draft file."""
    source = _read_text_if_exists(CODE_DRAFT_PATH).strip()

    if not source:
        source = (
            "# operator draft area is empty\n"
            "# write code into:\n"
            f"# {CODE_DRAFT_PATH}\n"
        )

    syntax = Syntax(
        source,
        "python",
        line_numbers=True,
        word_wrap=False,
        theme="monokai",
    )
    return Panel(syntax, title="Code Draft Area", border_style="cyan")


def _build_header_panel() -> Panel:
    """Build top header/status panel."""
    header_text = Group(
        Align.left(Text("MAKSIMAR OPERATOR INTERFACE [ACTIVE]", style="bold cyan")),
        Text(f"Project: {PROJECT_ROOT.name}", style="white"),
        Text(f"Wall clock: {time.strftime('%Y-%m-%d %H:%M:%S')}", style="white"),
        Text(
            f"Draft source: {CODE_DRAFT_PATH.name}",
            style="bright_black",
        ),
    )
    return Panel(header_text, border_style="cyan")


def build_live_layout() -> Layout:
    """Build full single-window live monitor layout."""
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body"),
        Layout(name="footer", size=5),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="center"),
        Layout(name="right"),
    )

    layout["left"].split_column(
        Layout(name="system_overview"),
        Layout(name="documents"),
    )
    layout["center"].split_column(
        Layout(name="platform_tree"),
        Layout(name="logs"),
    )
    layout["right"].split_column(
        Layout(name="worker_pulse"),
        Layout(name="code_area"),
    )

    layout["header"].update(_build_header_panel())
    layout["system_overview"].update(
        Panel(_build_system_overview_table(), title="System Overview", border_style="cyan")
    )
    layout["documents"].update(
        Panel(_build_documents_table(), title="Documents & Governance", border_style="cyan")
    )
    layout["platform_tree"].update(
        Panel(_build_platform_tree(), title="Platform Tree", border_style="cyan")
    )
    layout["logs"].update(_build_logs_panel())
    layout["worker_pulse"].update(
        Panel(_build_worker_table(), title="Worker Execution Pulse", border_style="cyan")
    )
    layout["code_area"].update(_build_code_panel())
    layout["footer"].update(
        Panel(
            Text(
                "Read-only Rich live HUD. Edit operator_code_draft.py and this pane will refresh automatically.",
                style="bright_black",
            ),
            title="Monitor Boundary",
            border_style="cyan",
        )
    )

    return layout


def render_once() -> None:
    """Render a single static frame."""
    from rich.console import Console

    console = Console()
    console.print(build_live_layout())


def run_live(refresh_per_second: float = 1.0) -> None:
    """Run live auto-refresh monitor."""
    with Live(build_live_layout(), refresh_per_second=refresh_per_second, screen=True) as live:
        while True:
            live.update(build_live_layout())
            time.sleep(max(0.5, 1.0 / refresh_per_second))


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Render one frame and exit.")
    parser.add_argument(
        "--refresh-per-second",
        type=float,
        default=1.0,
        help="Refresh rate for live mode.",
    )
    args = parser.parse_args()

    if args.once:
        render_once()
        return

    run_live(refresh_per_second=args.refresh_per_second)


if __name__ == "__main__":
    main()
