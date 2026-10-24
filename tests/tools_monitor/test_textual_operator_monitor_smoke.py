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


def test_operator_monitors_do_not_promote_absent_runtime_or_sample_metrics(monkeypatch):
    from tools.monitor import textual_operator_monitor as textual
    from tools.monitor import rich_live_operator_monitor as rich
    from SUPERVISOR import runtime_preflight
    from rich.console import Console
    observation = {
        "decision": {"classification": "clean_start", "healthy": False},
        "runtime_pid_identity": {"alive": False, "matches": False},
        "health": {"ok": False},
        "heartbeats": {"guard": {"fresh": False, "status": "stopped"}},
    }
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: observation)
    monkeypatch.setattr(textual, "_discover_pytest_workers", lambda: [])
    monkeypatch.setattr(rich, "_discover_pytest_workers", lambda: [])
    output = textual.build_worker_text()
    assert "ACTIVE" not in output
    assert "clean_start" in output
    assert "stopped" in output
    assert "nominal" not in textual.build_system_overview_text()
    console = Console(record=True, width=120)
    console.print(rich._build_worker_table())
    console.print(rich._build_system_overview_table())
    rendered = console.export_text()
    assert "ACTIVE" not in rendered
    assert "nominal" not in rendered
    assert "72%" not in rendered and "61%" not in rendered
    assert "clean_start" in rendered


def test_rich_runtime_monitor_uses_canonical_snapshot_paths_and_missing_is_not_clear(monkeypatch, tmp_path):
    from tools.monitor import rich_runtime_monitor as monitor
    from CORE_ROOT import runtime_paths
    preflight = tmp_path / "preflight_result.json"
    incident = tmp_path / "last_incident_snapshot.json"
    degraded = tmp_path / "degraded_mode.flag"
    monkeypatch.setattr(runtime_paths, "PREFLIGHT_RESULT_FILE", preflight)
    monkeypatch.setattr(runtime_paths, "INCIDENT_SNAPSHOT_FILE", incident)
    monkeypatch.setattr(runtime_paths, "DEGRADED_MODE_FILE", degraded)
    monkeypatch.setattr(runtime_paths, "RUNTIME_STATE_DIR", tmp_path / "missing")
    cards = monitor.build_status_cards()
    assert cards[0].value == "missing"
    assert cards[2].value == "unknown"
    monkeypatch.setattr(runtime_paths, "RUNTIME_STATE_DIR", tmp_path)
    preflight.write_text('{"ok": false}', encoding="utf-8")
    incident.write_text('{"kind": "retained_incident"}', encoding="utf-8")
    degraded.write_text("1", encoding="utf-8")
    cards = monitor.build_status_cards()
    assert cards[0].value == "failed"
    assert cards[1].value == "present"
    assert cards[2].value == "active"
