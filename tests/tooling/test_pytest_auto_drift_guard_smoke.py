from __future__ import annotations

from pathlib import Path


def test_pytest_auto_drift_guard_is_installed() -> None:
    text = Path("conftest.py").read_text(encoding="utf-8")

    assert "pytest_sessionstart" in text
    assert "tools/git_stage_guard.py" in text
    assert "tools/roadmap_pre_step_check.py" in text
    assert "--inventory-only" in text
    assert "tools/roadmap_post_step_drift_check.py" in text
    assert "PYTEST_XDIST_WORKER" in text
    assert "MAKSIMAR_SKIP_PYTEST_DRIFT_GUARD" in text
