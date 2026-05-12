from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_module_flow


def test_final_memory_module_flow_builder_smoke() -> None:
    flow = build_final_memory_module_flow()

    assert flow["module_flow_ready"] is True
    assert flow["all_registered_modules_visible"] is True
    assert "dashboard_read_only_preview" in flow["flow"]
