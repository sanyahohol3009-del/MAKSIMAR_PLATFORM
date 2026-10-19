from __future__ import annotations

import importlib
import pytest


@pytest.mark.parametrize("decision", [True, False, RuntimeError("observer unavailable")])
def test_recovery_cli_delegates_marker_decision_to_canonical_owner(monkeypatch, tmp_path, decision):
    manager = importlib.import_module("RUNTIME.recovery_manager")
    canonical = importlib.import_module("CORE_ROOT.stop_gate")
    stale_legacy_flag = tmp_path / "degraded_mode.flag"
    stale_legacy_flag.write_text("retained legacy diagnostic")
    # Old status-only code must not touch a legacy flag or authorize recovery.
    monkeypatch.setattr(manager, "DEGRADED_FLAG", stale_legacy_flag, raising=False)
    monkeypatch.setattr(manager, "load_json", lambda path: {"source": "foreign_process", "status": "alive", "ts": __import__("time").time()}, raising=False)
    logs = []
    monkeypatch.setattr(manager, "log", logs.append)
    calls = []

    def recover():
        calls.append("canonical")
        if isinstance(decision, Exception):
            raise decision
        return decision

    monkeypatch.setattr(canonical, "recover_previous_run_degradation", recover)
    manager.main()
    assert calls == ["canonical"]
    assert stale_legacy_flag.read_text() == "retained legacy diagnostic"
    assert any("Recovery OK" in line for line in logs) is (decision is True)
    if decision is False:
        assert any("Recovery skipped" in line for line in logs)
    if isinstance(decision, Exception):
        assert any("Recovery manager failed" in line for line in logs)
