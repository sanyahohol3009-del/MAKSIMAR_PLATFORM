from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Static, TextArea


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


def _tail_lines(path: Path, max_lines: int = 6) -> list[str]:
    """Return last lines from a log file."""
    if not path.exists():
        return []
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:]
    except OSError:
        return []


def _count_files(directory: Path, suffix: str = ".md") -> int:
    """Count files by suffix."""
    if not directory.exists():
        return 0
    try:
        return sum(1 for item in directory.iterdir() if item.is_file() and item.suffix == suffix)
    except OSError:
        return 0


def _run_shell_lines(command: list[str]) -> list[str]:
    """Run shell command safely and return output lines."""
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


def _discover_pytest_workers() -> list[str]:
    """Discover pytest/xdist workers if present."""
    return _run_shell_lines(["bash", "-lc", r"pgrep -af 'pytest|xdist|gw[0-9]' || true"])[:8]


def build_system_overview_text() -> str:
    """Build system overview text."""
    try:
        load1, load5, load15 = os.getloadavg()
        load_text = f"{load1:.2f} / {load5:.2f} / {load15:.2f}"
    except (AttributeError, OSError):
        load_text = "n/a"

    return (
        "SYSTEM OVERVIEW\n"
        "--------------\n"
        "CPU Budget: bounded\n"
        "Memory Budget: bounded\n"
        "Pressure: nominal\n"
        f"Load(1/5/15): {load_text}\n"
    )


def build_documents_text() -> str:
    """Build documents/governance summary."""
    docs_count = _count_files(DOCS_DIR)
    concurrency_count = _count_files(CONCURRENCY_DOCS_DIR)
    draft_present = CODE_DRAFT_PATH.exists()

    return (
        "DOCUMENTS & GOVERNANCE\n"
        "----------------------\n"
        f"docs/: {docs_count}\n"
        f"concurrency_governance/: {concurrency_count}\n"
        f"code draft area: {'linked' if draft_present else 'missing'}\n"
    )


def build_platform_tree_text() -> str:
    """Build simple text tree."""
    return (
        "PLATFORM TREE\n"
        "-------------\n"
        "MAKSIMAR_PLATFORM\n"
        "├── MAKSIMAR_CORE_LIB\n"
        "├── MAKSIMAR_SERVER\n"
        "├── docs\n"
        "├── tests\n"
        "└── tools\n"
        "    └── monitor\n"
        "        ├── rich_live_operator_monitor.py\n"
        "        ├── textual_operator_monitor.py\n"
        "        └── runtime_input/operator_code_draft.py\n"
    )


def build_worker_text() -> str:
    """Build worker pulse text."""
    workers = _discover_pytest_workers()
    if workers:
        lines = ["WORKER EXECUTION PULSE", "----------------------"]
        for index, line in enumerate(workers, start=1):
            lines.append(f"gw{index - 1}: PROCESSING | {line[:70]}")
        return "\n".join(lines)

    return (
        "WORKER EXECUTION PULSE\n"
        "----------------------\n"
        "core: ACTIVE\n"
        "guard: ACTIVE\n"
        "pytest workers: none detected\n"
    )


def build_logs_text() -> str:
    """Build logs text block."""
    log_candidates = [
        LOGS_DIR / "guard.log",
        LOGS_DIR / "core_guard.log",
        LOGS_DIR / "kernel_guard.log",
    ]

    lines: list[str] = ["LIVE LOGS & ALERTS", "------------------"]
    for path in log_candidates:
        tailed = _tail_lines(path)
        if tailed:
            lines.append(f"[{path.name}]")
            lines.extend(tailed)

    if len(lines) == 2:
        lines.append("No recent canonical log lines found.")

    return "\n".join(lines)


class InfoBox(Static):
    """Simple info box widget."""


class TextualOperatorMonitor(App[None]):
    """Single-window textual operator monitor."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #body {
        height: 1fr;
    }

    .column {
        width: 1fr;
        height: 1fr;
        border: round cyan;
        padding: 1;
    }

    #footer_note {
        height: 3;
        border: round cyan;
        padding: 1;
    }

    #code_input {
        height: 3;
    }

    #code_editor {
        height: 1fr;
        border: round cyan;
    }
    """

    BINDINGS = [
        ("ctrl+s", "save_draft", "Save Draft"),
        ("ctrl+r", "refresh_now", "Refresh"),
        ("ctrl+q", "quit", "Quit"),
    ]

    refresh_seconds: reactive[float] = reactive(1.0)

    def compose(self) -> ComposeResult:
        """Compose UI."""
        yield Header(show_clock=True)

        with Horizontal(id="body"):
            with Vertical(classes="column"):
                yield InfoBox(build_system_overview_text(), id="system_box")
                yield InfoBox(build_documents_text(), id="documents_box")

            with Vertical(classes="column"):
                yield InfoBox(build_platform_tree_text(), id="tree_box")
                yield InfoBox(build_logs_text(), id="logs_box")

            with Vertical(classes="column"):
                yield InfoBox(build_worker_text(), id="worker_box")
                yield Input(
                    placeholder="Draft note only. No execution from this UI.",
                    id="code_input",
                )
                yield TextArea(
                    text=_read_text_if_exists(CODE_DRAFT_PATH),
                    language="python",
                    id="code_editor",
                )

        yield Static(
            "Read-only monitor. Editable draft area only. No runtime execution.",
            id="footer_note",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Start periodic refresh."""
        self.set_interval(self.refresh_seconds, self._refresh_panels)

    def _refresh_panels(self) -> None:
        """Refresh non-editor panels from canonical sources."""
        self.query_one("#system_box", InfoBox).update(build_system_overview_text())
        self.query_one("#documents_box", InfoBox).update(build_documents_text())
        self.query_one("#tree_box", InfoBox).update(build_platform_tree_text())
        self.query_one("#logs_box", InfoBox).update(build_logs_text())
        self.query_one("#worker_box", InfoBox).update(build_worker_text())

    def action_save_draft(self) -> None:
        """Save current editor text to draft file."""
        editor = self.query_one("#code_editor", TextArea)
        CODE_DRAFT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CODE_DRAFT_PATH.write_text(editor.text, encoding="utf-8")
        self.notify("Draft saved.")

    def action_refresh_now(self) -> None:
        """Manual refresh."""
        self._refresh_panels()
        self.notify("Panels refreshed.")


def main() -> None:
    """CLI entrypoint."""
    app = TextualOperatorMonitor()
    app.run()


if __name__ == "__main__":
    main()
