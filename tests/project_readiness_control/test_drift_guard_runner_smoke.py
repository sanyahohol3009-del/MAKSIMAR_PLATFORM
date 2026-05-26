from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.drift_guard_runner as runner


def test_drift_guard_runner_wraps_existing_post_step_check(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(
            returncode=0,
            stdout='{"drift_check_passed": true}',
            stderr="",
        )

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_drift_guard(python_executable="./.venv/bin/python")

    assert result.returncode == 0
    assert result.drift_check_passed is True
    assert result.command == (
        "./.venv/bin/python",
        "tools/roadmap_post_step_drift_check.py",
    )
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert captured["kwargs"]["shell"] is False
