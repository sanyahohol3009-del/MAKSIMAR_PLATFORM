from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_models import (
    LayoutCompositionContract,
    LayoutCompositionEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def build_layout_composition_contract() -> LayoutCompositionContract:
    """Build the canonical layout composition contract."""
    workspace_contract = build_workspace_registry_contract()

    slot_map: dict[str, tuple[str, ...]] = {
        "workspace_foundation_monitoring": (
            "slot_foundation_main_0",
            "slot_foundation_main_1",
            "slot_foundation_main_2",
            "slot_foundation_secondary_0",
            "slot_foundation_secondary_1",
        ),
        "workspace_operator_interaction": (
            "slot_operator_main_0",
            "slot_operator_main_1",
            "slot_operator_main_2",
        ),
    }

    zone_map: dict[str, str] = {
        "workspace_foundation_monitoring": "foundation_layout_zone",
        "workspace_operator_interaction": "operator_layout_zone",
    }

    entries: list[LayoutCompositionEntry] = []

    for workspace_entry in workspace_contract.entries:
        slots = slot_map[workspace_entry.workspace_id]
        zone = zone_map[workspace_entry.workspace_id]

        for index, panel_id in enumerate(workspace_entry.included_panel_ids):
            entries.append(
                LayoutCompositionEntry(
                    workspace_id=workspace_entry.workspace_id,
                    panel_id=panel_id,
                    layout_slot_id=slots[index],
                    layout_zone=zone,
                    slot_order=index,
                    description=(
                        f"Canonical layout composition entry for {panel_id} "
                        f"in {workspace_entry.workspace_id}."
                    ),
                )
            )

    return LayoutCompositionContract(entries=tuple(entries))
