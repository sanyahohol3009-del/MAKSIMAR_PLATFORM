from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_phase_readiness,
)


_FORBIDDEN_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
)


def test_phase_3_2_no_new_roots_smoke() -> None:
    readiness = build_presentation_phase_readiness()

    assert readiness.no_new_presentation_roots is True

    for root_name in _FORBIDDEN_ROOTS:
        assert not Path(root_name).exists()
