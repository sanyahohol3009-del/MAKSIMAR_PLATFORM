from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_final_memory_map_ready_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["acceptance_ready"] is True
    assert acceptance["project_fully_visible_in_memory"] is True
    assert acceptance["dashboard_read_only"] is True
    assert acceptance["canonical_write_allowed"] is False
    assert acceptance["runtime_mutation_allowed"] is False
