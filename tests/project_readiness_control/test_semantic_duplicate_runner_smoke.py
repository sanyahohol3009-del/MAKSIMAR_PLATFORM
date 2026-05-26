from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.semantic_duplicate_scan_runner as runner


def test_semantic_duplicate_runner_wraps_existing_preview_tool(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="semantic ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    result = runner.run_semantic_duplicate_scan(python_executable="./.venv/bin/python")

    assert result.returncode == 0
    assert "tools/root_artifact_semantic_duplicate_preview.py" in result.command
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert captured["kwargs"]["shell"] is False
