from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_zone_vocabulary_models import (
    PanelZoneEntry,
    PanelZoneVocabularyContract,
)


def test_panel_zone_entry_smoke() -> None:
    entry = PanelZoneEntry(
        layout_zone="foundation_layout_zone",
        layout_slot_id="slot_foundation_main_0",
        slot_family="foundation_main",
        slot_order=0,
        description="Zone description.",
    )

    assert entry.layout_slot_id == "slot_foundation_main_0"


def test_panel_zone_vocabulary_contract_rejects_duplicates() -> None:
    entry_a = PanelZoneEntry(
        layout_zone="foundation_layout_zone",
        layout_slot_id="slot_foundation_main_0",
        slot_family="foundation_main",
        slot_order=0,
        description="A",
    )
    entry_b = PanelZoneEntry(
        layout_zone="foundation_layout_zone",
        layout_slot_id="slot_foundation_main_0",
        slot_family="foundation_main",
        slot_order=1,
        description="B",
    )

    with pytest.raises(
        ValueError,
        match="duplicate layout_zone/layout_slot_id detected",
    ):
        PanelZoneVocabularyContract(entries=(entry_a, entry_b))
