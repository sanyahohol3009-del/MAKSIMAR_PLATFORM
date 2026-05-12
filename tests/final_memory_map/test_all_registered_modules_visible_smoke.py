from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_all_registered_modules_visible_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["all_registered_modules_visible"] is True
