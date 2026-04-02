from __future__ import annotations

from tools.monitor.textual_operator_monitor import (
    TextualOperatorMonitor,
    build_documents_text,
    build_logs_text,
    build_platform_tree_text,
    build_system_overview_text,
    build_worker_text,
)


def test_build_system_overview_text_builds() -> None:
    """System overview text should build successfully."""
    text = build_system_overview_text()
    assert "SYSTEM OVERVIEW" in text


def test_build_documents_text_builds() -> None:
    """Documents text should build successfully."""
    text = build_documents_text()
    assert "DOCUMENTS & GOVERNANCE" in text


def test_build_platform_tree_text_builds() -> None:
    """Platform tree text should build successfully."""
    text = build_platform_tree_text()
    assert "MAKSIMAR_PLATFORM" in text


def test_build_worker_text_builds() -> None:
    """Worker text should build successfully."""
    text = build_worker_text()
    assert "WORKER EXECUTION PULSE" in text


def test_build_logs_text_builds() -> None:
    """Logs text should build successfully."""
    text = build_logs_text()
    assert "LIVE LOGS & ALERTS" in text


def test_textual_operator_monitor_instantiates() -> None:
    """Textual operator monitor should instantiate successfully."""
    app = TextualOperatorMonitor()
    assert app is not None
