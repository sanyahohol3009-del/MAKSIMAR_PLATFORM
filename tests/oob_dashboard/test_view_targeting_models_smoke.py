from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_models import (
    ViewTargetingContract,
    ViewTargetingEntry,
)


def test_view_targeting_entry_smoke() -> None:
    entry = ViewTargetingEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        view_target_kind="foundation_view",
        view_scope="foundation",
        description="View description.",
    )

    assert entry.panel_id == "system_status"


def test_view_targeting_contract_rejects_duplicates() -> None:
    entry_a = ViewTargetingEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        view_target_kind="foundation_view",
        view_scope="foundation",
        description="A",
    )
    entry_b = ViewTargetingEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        view_target_kind="foundation_view",
        view_scope="foundation",
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        ViewTargetingContract(entries=(entry_a, entry_b))
