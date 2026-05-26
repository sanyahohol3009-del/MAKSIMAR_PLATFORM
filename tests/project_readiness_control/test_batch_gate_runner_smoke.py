from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.batch_gate_runner as runner
from tools.project_readiness_control.target_test_runner import TargetTestRunResult


def test_batch_gate_runner_reuses_readiness_map_and_target_runner(monkeypatch) -> None:
    captured = {}

    def fake_subprocess_run(command, **kwargs):
        captured["readiness_command"] = command
        captured["readiness_kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="status=READY", stderr="")

    def fake_target_runner(target_paths, *, python_executable=None):
        captured["target_paths"] = tuple(target_paths)
        captured["python_executable"] = python_executable
        return TargetTestRunResult(
            command=("./.venv/bin/python", "-m", "pytest", "target", "-q"),
            target_paths=tuple(target_paths),
            returncode=0,
            stdout="ok",
            stderr="",
        )

    monkeypatch.setattr(runner.subprocess, "run", fake_subprocess_run)
    monkeypatch.setattr(runner, "run_target_tests", fake_target_runner)

    result = runner.run_batch_gate(
        batch_id="0.5",
        target_paths=("tests/project_readiness_control/test_target_test_runner_smoke.py",),
        python_executable="./.venv/bin/python",
    )

    assert result.passed is True
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert captured["readiness_command"] == (
        "./.venv/bin/python",
        "tools/project_readiness_control/project_file_readiness_map.py",
        "--batch-id",
        "0.5",
    )
    assert captured["readiness_kwargs"]["shell"] is False
    assert captured["target_paths"] == (
        "tests/project_readiness_control/test_target_test_runner_smoke.py",
    )
