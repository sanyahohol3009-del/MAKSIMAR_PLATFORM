from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_phase_readiness,
)


_FORBIDDEN_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
)


def test_phase_3_1_no_new_roots_smoke() -> None:
    readiness = build_display_topology_phase_readiness()

    assert readiness.no_new_display_roots is True

    for root_name in _FORBIDDEN_ROOTS:
        assert not Path(root_name).exists()
