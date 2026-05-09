from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_preview,
)


def test_dashboard_read_only_views_batch2_ready_smoke() -> None:
    contract = build_dashboard_read_only_views_contract()
    preview = build_memory_registry_view_preview()

    assert preview["preview_ready"] is True
    assert contract.total_entries == 2 + preview["total_views"]
    assert contract.active_entries == contract.total_entries
    assert contract.multilingual_ready_entries == contract.total_entries
    assert contract.explanation_available_entries == contract.total_entries
