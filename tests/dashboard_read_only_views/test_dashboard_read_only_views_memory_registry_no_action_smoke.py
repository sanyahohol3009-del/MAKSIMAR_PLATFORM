from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)


def test_dashboard_read_only_views_memory_registry_no_action_smoke() -> None:
    contract = build_dashboard_read_only_views_contract()

    for entry in contract.entries:
        assert entry.read_only_mode == "read_only"

    for entry in contract.entries:
        if entry.view_kind == "memory_registry_read_only_view":
            assert entry.linked_skill_id == ""
            assert entry.panel_id.startswith("panel_memory_")
            assert entry.display_role == "mobile_display_proxy"
