from __future__ import annotations

import importlib
import pytest


@pytest.mark.parametrize("decision", [True, False, RuntimeError("observer unavailable")])
def test_recovery_cli_delegates_marker_decision_to_canonical_owner(monkeypatch, tmp_path, decision):
    manager = importlib.import_module("RUNTIME.recovery_manager")
    canonical = importlib.import_module("SUPERVISOR.runtime_preflight")
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


@pytest.mark.parametrize("decision", [True, False])
def test_work_embedded_command_calls_same_supervisor_entrypoint(monkeypatch, decision):
    from pathlib import Path
    from SUPERVISOR import runtime_preflight
    text = (Path(__file__).resolve().parents[2] / "tools/work").read_text()
    body = text.split("recover_previous_run_degradation() {\n", 1)[1].split("\n}", 1)[0]
    command = body.split("'", 2)[1]
    calls = []
    monkeypatch.setattr(runtime_preflight, "recover_previous_run_degradation", lambda: calls.append("canonical") or decision)
    with pytest.raises(SystemExit) as error:
        exec(compile(command, "tools/work::recover_previous_run_degradation", "exec"), {})
    assert error.value.code == (0 if decision else 1)
    assert calls == ["canonical"]
    assert '|| log "degradation remains active:' in body


from tests.runtime.test_previous_run_degradation_recovery import environment


@pytest.mark.parametrize("current_marker", [False, True])
def test_recovery_cli_real_canonical_transaction(environment, monkeypatch, current_marker):
    import os
    manager = importlib.import_module("RUNTIME.recovery_manager")
    flag, _, trigger, reason, records = environment
    if current_marker:
        os.utime(flag, ns=(3_000_000_000,) * 2)
    logs = []
    monkeypatch.setattr(manager, "log", logs.append)
    manager.main()
    assert flag.exists() is current_marker
    assert any("Recovery OK" in line for line in logs) is (not current_marker)
    assert any("Recovery skipped" in line for line in logs) is current_marker
    assert trigger.read_text() == "original incident evidence"
    assert reason.read_text() == "historical heartbeat timeout"
    assert [status for _, status in records] == ([] if current_marker else ["recovery_pending", "recovered"])
