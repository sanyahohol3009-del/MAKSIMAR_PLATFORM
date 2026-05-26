from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.full_platform_auto_runner as runner


def test_full_platform_auto_runner_requires_explicit_report_gate(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_full_platform_auto(
        python_executable="./.venv/bin/python",
        base_env={"KEEP": "yes"},
    )

    assert result.returncode == 0
    assert result.full_platform_reports_enabled is True
    assert "--maksimar-full-platform-reports" in result.command
    assert captured["command"] == (
        "./.venv/bin/python",
        "-m",
        "pytest",
        "-q",
        "-n",
        "auto",
        "--maksimar-full-platform-reports",
    )
    assert captured["kwargs"]["shell"] is False
    assert captured["kwargs"]["env"]["MAKSIMAR_FULL_PLATFORM_REPORTS"] == "1"
    assert captured["kwargs"]["env"]["KEEP"] == "yes"
