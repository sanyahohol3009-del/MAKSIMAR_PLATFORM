from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.roadmap_ci_runner as runner


def test_roadmap_ci_runner_wraps_existing_ci_tool(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="roadmap ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_roadmap_ci(python_executable="./.venv/bin/python")

    assert result.returncode == 0
    assert result.command == (
        "./.venv/bin/python",
        "tools/foundation_roadmap_ci_check.py",
    )
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert captured["kwargs"]["shell"] is False
