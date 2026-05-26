from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.target_test_runner as runner


def test_target_test_runner_keeps_pytest_quiet(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_target_tests(
        ("tests/vendor_security_gate/test_repository_scan_runtime_smoke.py",),
        python_executable="./.venv/bin/python",
        base_env={"MAKSIMAR_FULL_PLATFORM_REPORTS": "1", "KEEP": "yes"},
    )

    assert result.returncode == 0
    assert result.full_platform_reports_enabled is False
    assert "--maksimar-full-platform-reports" not in result.command
    assert captured["command"] == (
        "./.venv/bin/python",
        "-m",
        "pytest",
        "tests/vendor_security_gate/test_repository_scan_runtime_smoke.py",
        "-q",
    )
    assert captured["kwargs"]["shell"] is False
    assert "MAKSIMAR_FULL_PLATFORM_REPORTS" not in captured["kwargs"]["env"]
    assert captured["kwargs"]["env"]["KEEP"] == "yes"
