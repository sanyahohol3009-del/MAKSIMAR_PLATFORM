from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_models import (
    PanelViewDisplayChainContract,
    PanelViewDisplayChainEntry,
)


def test_panel_view_display_chain_entry_smoke() -> None:
    entry = PanelViewDisplayChainEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        display_role="foundation_primary_display",
        display_zone="foundation_main_zone",
        is_default_chain=True,
        description="Chain description.",
    )

    assert entry.panel_id == "system_status"


def test_panel_view_display_chain_contract_rejects_duplicates() -> None:
    entry_a = PanelViewDisplayChainEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        display_role="foundation_primary_display",
        display_zone="foundation_main_zone",
        is_default_chain=True,
        description="A",
    )
    entry_b = PanelViewDisplayChainEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        display_role="foundation_primary_display",
        display_zone="foundation_main_zone",
        is_default_chain=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelViewDisplayChainContract(entries=(entry_a, entry_b))
