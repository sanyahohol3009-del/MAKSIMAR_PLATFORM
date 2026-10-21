from __future__ import annotations

import importlib
from pathlib import Path


def test_stop_gate_watcher_log_writes_to_file(tmp_path: Path) -> None:
    module = importlib.import_module("CORE_ROOT.stop_gate_watcher")
    target_log = tmp_path / "guard.log"
    system_log = tmp_path / "system.log"

    module.GUARD_LOG_FILE = target_log
    module.SYSTEM_LOG_FILE = system_log
    module.ensure_runtime_layout = lambda: None

    module.log("watcher deep test")

    assert target_log.exists()
    assert system_log.exists()
    assert "watcher deep test" in target_log.read_text(encoding="utf-8")
    assert "watcher deep test" in system_log.read_text(encoding="utf-8")


def test_stop_gate_watcher_evaluate_runtime_returns_tuple_when_heartbeat_missing(tmp_path: Path, monkeypatch) -> None:
    module = importlib.import_module("CORE_ROOT.stop_gate_watcher")
    monkeypatch.setattr(module, "RUNTIME_HEARTBEAT_FILE", tmp_path / "absent_runtime_heartbeat.json")
    result = module.evaluate_runtime(
        started_at=module.time.time(),
        source_mismatch_strikes=0,
    )

    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)
    assert isinstance(result[2], int)


def test_stop_gate_watcher_activate_guard_kill_chain_writes_stopped_heartbeat(tmp_path: Path) -> None:
    module = importlib.import_module("CORE_ROOT.stop_gate_watcher")

    module.GUARD_LOG_FILE = tmp_path / "guard.log"
    module.SYSTEM_LOG_FILE = tmp_path / "system.log"
    module.GUARD_HEARTBEAT_FILE = tmp_path / "guard_heartbeat.json"
    module.ensure_runtime_layout = lambda: None

    original_run_quiet = module.run_quiet
    try:
        module.run_quiet = lambda *args, **kwargs: None
        module.activate_guard_kill_chain("deep watcher reason")
    finally:
        module.run_quiet = original_run_quiet

    assert module.GUARD_HEARTBEAT_FILE.exists()
    content = module.GUARD_HEARTBEAT_FILE.read_text(encoding="utf-8")
    assert '"status":"stopped"' in content
