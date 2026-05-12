from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_preview


def test_final_memory_preview_builder_smoke() -> None:
    preview = build_final_memory_preview()

    assert preview["preview_ready"] is True
    assert preview["dashboard_read_only"] is True
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
