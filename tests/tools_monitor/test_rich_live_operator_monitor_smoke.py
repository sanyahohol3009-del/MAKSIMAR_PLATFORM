from __future__ import annotations

from tools.monitor.rich_live_operator_monitor import (
    _build_code_panel,
    _build_documents_table,
    _build_platform_tree,
    _build_system_overview_table,
    _build_worker_table,
    build_live_layout,
)


def test_build_system_overview_table_builds() -> None:
    """System overview table should build successfully."""
    table = _build_system_overview_table()
    assert table is not None


def test_build_platform_tree_builds() -> None:
    """Platform tree should build successfully."""
    tree = _build_platform_tree()
    assert tree.label == "[bold cyan]MAKSIMAR_PLATFORM[/bold cyan]"


def test_build_worker_table_builds() -> None:
    """Worker execution table should build successfully."""
    table = _build_worker_table()
    assert table is not None


def test_build_documents_table_builds() -> None:
    """Documents table should build successfully."""
    table = _build_documents_table()
    assert table is not None


def test_build_code_panel_builds() -> None:
    """Code panel should build successfully."""
    panel = _build_code_panel()
    assert panel.title == "Code Draft Area"


def test_build_live_layout_builds() -> None:
    """Full live layout should build successfully."""
    layout = build_live_layout()
    assert layout is not None
