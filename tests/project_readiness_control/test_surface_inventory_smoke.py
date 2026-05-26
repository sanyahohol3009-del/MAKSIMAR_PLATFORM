from __future__ import annotations

import tools.project_readiness_control.surface_inventory as runner


def test_surface_inventory_reuses_existing_project_surface_audit(monkeypatch) -> None:
    monkeypatch.setattr(runner, "build_project_surface_inventory", lambda root: ())
    monkeypatch.setattr(
        runner,
        "build_project_surface_summary",
        lambda root: {
            "total_surfaces": 3,
            "tracked_surfaces": 2,
            "untracked_surfaces": 1,
            "critical_surfaces_present": True,
        },
    )

    result = runner.run_surface_inventory(".")

    assert result.total_surfaces == 3
    assert result.tracked_surfaces == 2
    assert result.untracked_surfaces == 1
    assert result.critical_surfaces_present is True
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
    assert "project_surface_audit" in result.source_surface
