from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_phase_readiness,
)


_FORBIDDEN_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
    "MAKSIMAR_CORE_LIB/memory_engine/explainable_view_binding",
)


def test_phase_3_3_no_new_roots_smoke() -> None:
    readiness = build_explainable_phase_readiness()

    assert readiness.no_new_explainability_roots is True

    for root_name in _FORBIDDEN_ROOTS:
        assert not Path(root_name).exists()
