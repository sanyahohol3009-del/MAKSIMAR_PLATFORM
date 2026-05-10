from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_router_contract,
)


def test_multi_display_selection_smoke() -> None:
    contract = build_presentation_router_contract()

    selected_display_ids = tuple(entry.selected_display_id for entry in contract.entries)
    selected_zone_ids = tuple(entry.selected_zone_id for entry in contract.entries)

    assert selected_display_ids == (
        "display_mobile_proxy_001",
        "display_engineering_001",
        "display_primary_dashboard_001",
    )
    assert selected_zone_ids == (
        "zone_mobile_main",
        "zone_engineering_main",
        "zone_dashboard_main",
    )
    assert len(set(selected_display_ids)) == 3
