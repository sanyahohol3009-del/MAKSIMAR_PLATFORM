from __future__ import annotations

from types import SimpleNamespace

import tools.project_readiness_control.acceptance_evidence_collector as collector


def test_acceptance_evidence_collector_reuses_existing_surfaces(monkeypatch) -> None:
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="status=READY\nfiles=6/6\n", stderr="")

    monkeypatch.setattr(collector.subprocess, "run", fake_run)
    monkeypatch.setattr(
        collector,
        "run_surface_inventory",
        lambda root: SimpleNamespace(
            total_surfaces=10,
            tracked_surfaces=8,
            untracked_surfaces=2,
            critical_surfaces_present=True,
        ),
    )
    monkeypatch.setattr(
        collector,
        "classify_dirty_surfaces",
        lambda project_root: SimpleNamespace(dirty_count=3, untracked_count=2),
    )

    result = collector.collect_acceptance_evidence(
        batch_id="0.7",
        python_executable="./.venv/bin/python",
    )

    assert result.read_model.status == "READY"
    assert result.read_model.evidence_count == 3
    assert result.read_model.warning_count == 1
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert result.shell_execution_allowed is False
    assert captured["command"] == (
        "./.venv/bin/python",
        "tools/project_readiness_control/project_file_readiness_map.py",
        "--batch-id",
        "0.7",
    )
    assert captured["kwargs"]["shell"] is False
