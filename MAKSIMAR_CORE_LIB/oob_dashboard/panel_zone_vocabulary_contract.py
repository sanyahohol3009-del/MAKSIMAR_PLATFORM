from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_zone_vocabulary_models import (
    PanelZoneEntry,
    PanelZoneVocabularyContract,
)


def resolve_slot_family(layout_slot_id: str) -> str:
    """Resolve the canonical slot family for a layout slot."""
    if layout_slot_id.startswith("slot_foundation_main_"):
        return "foundation_main"

    if layout_slot_id.startswith("slot_foundation_secondary_"):
        return "foundation_secondary"

    if layout_slot_id.startswith("slot_operator_main_"):
        return "operator_main"

    raise ValueError(f"unsupported layout_slot_id for slot_family: {layout_slot_id}")


def build_panel_zone_vocabulary_contract() -> PanelZoneVocabularyContract:
    """Build the canonical panel zone / slot vocabulary contract."""
    layout_contract = build_layout_composition_contract()

    seen: set[tuple[str, str]] = set()
    entries: list[PanelZoneEntry] = []

    for entry in layout_contract.entries:
        key = (entry.layout_zone, entry.layout_slot_id)
        if key in seen:
            continue
        seen.add(key)

        entries.append(
            PanelZoneEntry(
                layout_zone=entry.layout_zone,
                layout_slot_id=entry.layout_slot_id,
                slot_family=resolve_slot_family(entry.layout_slot_id),
                slot_order=entry.slot_order,
                description=(
                    f"Canonical zone-slot vocabulary entry for "
                    f"{entry.layout_zone}/{entry.layout_slot_id}."
                ),
            )
        )

    return PanelZoneVocabularyContract(entries=tuple(entries))
