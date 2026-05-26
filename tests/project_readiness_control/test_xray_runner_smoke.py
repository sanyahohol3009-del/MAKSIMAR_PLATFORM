from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.xray_runner as runner


def test_xray_runner_wraps_existing_xray_tool(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="xray ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_xray(python_executable="./.venv/bin/python")

    assert result.returncode == 0
    assert result.command == (
        "./.venv/bin/python",
        "tools/architecture_xray_radar.py",
    )
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert captured["kwargs"]["shell"] is False
