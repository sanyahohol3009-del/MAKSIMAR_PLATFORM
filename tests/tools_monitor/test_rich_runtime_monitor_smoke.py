from __future__ import annotations

from rich.console import Console

from tools.monitor.rich_runtime_monitor import (
    build_status_cards,
    build_status_table,
    build_logs_panel,
    render_monitor,
)


def test_build_status_cards_returns_cards() -> None:
    """Status cards builder should return a non-empty list."""
    cards = build_status_cards()

    assert len(cards) == 3
    assert cards[0].title == "Preflight"
    assert cards[1].title == "Incident"
    assert cards[2].title == "Degraded"


def test_build_status_table_has_expected_title() -> None:
    """Status table should build successfully."""
    table = build_status_table()

    assert table.title == "MAKSIMAR Read-Only Monitor"


def test_build_logs_panel_builds() -> None:
    """Logs panel should build successfully."""
    panel = build_logs_panel()

    assert panel.title == "Recent Logs"


def test_render_monitor_runs() -> None:
    """Render monitor should execute without errors."""
    console = Console(record=True, width=120)
    render_monitor(console=console)

    output = console.export_text()
    assert "MAKSIMAR Read-Only Monitor" in output
