from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_models import (
    LayoutCompositionContract,
    LayoutCompositionEntry,
)


def test_layout_composition_entry_smoke() -> None:
    entry = LayoutCompositionEntry(
        workspace_id="workspace_foundation_monitoring",
        panel_id="system_status",
        layout_slot_id="slot_foundation_main_0",
        layout_zone="foundation_layout_zone",
        slot_order=0,
        description="Layout description.",
    )

    assert entry.panel_id == "system_status"


def test_layout_composition_contract_smoke() -> None:
    contract = LayoutCompositionContract(
        entries=(
            LayoutCompositionEntry(
                workspace_id="workspace_foundation_monitoring",
                panel_id="system_status",
                layout_slot_id="slot_foundation_main_0",
                layout_zone="foundation_layout_zone",
                slot_order=0,
                description="Layout description.",
            ),
        )
    )

    assert len(contract.entries) == 1
