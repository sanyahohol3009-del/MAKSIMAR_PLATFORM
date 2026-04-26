from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_models import (
    PanelRegistryContract,
    PanelRegistryEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_vocabulary_contract import (
    build_panel_vocabulary_contract,
)


def build_panel_registry_contract() -> PanelRegistryContract:
    """Build the canonical panel registry contract."""
    vocabulary = build_panel_vocabulary_contract()

    entries = tuple(
        PanelRegistryEntry(
            panel_id=entry.panel_id,
            title=entry.title,
            panel_family=entry.panel_family,
            panel_kind=entry.panel_kind,
            source_binding_required=True,
            visibility_policy_required=True,
        )
        for entry in vocabulary.entries
    )

    contract = PanelRegistryContract(entries=entries)

    canonical_ids = build_canonical_panel_ids()
    registry_ids = tuple(entry.panel_id for entry in contract.entries)
    if registry_ids != canonical_ids:
        raise ValueError("panel registry order must match canonical panel id order")

    return contract
