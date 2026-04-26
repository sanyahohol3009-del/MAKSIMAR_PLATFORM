from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_models import (
    PanelBindingContract,
    PanelBindingEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


def resolve_display_target_id(panel_id: str) -> str:
    """Resolve the canonical display target for a panel."""
    foundation_targets = {
        "system_status": "display_foundation_primary",
        "guard_chain": "display_foundation_primary",
        "incidents": "display_foundation_primary",
        "logs": "display_foundation_secondary",
        "topology": "display_foundation_secondary",
    }
    interaction_targets = {
        "action_queue": "display_operator_interaction",
        "approval_queue": "display_operator_interaction",
        "audit_timeline": "display_operator_interaction",
    }

    if panel_id in foundation_targets:
        return foundation_targets[panel_id]

    if panel_id in interaction_targets:
        return interaction_targets[panel_id]

    raise ValueError(f"unsupported panel_id for binding: {panel_id}")


def resolve_binding_reason(panel_id: str) -> str:
    """Resolve the canonical binding reason for a panel."""
    if panel_id in {
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    }:
        return "foundation_visibility"

    if panel_id in {
        "action_queue",
        "approval_queue",
        "audit_timeline",
    }:
        return "operator_interaction_visibility"

    raise ValueError(f"unsupported panel_id for binding reason: {panel_id}")


def build_panel_binding_contract() -> PanelBindingContract:
    """Build the canonical panel-binding contract."""
    metadata_contract = build_panel_metadata_contract()
    exposure_contract = build_panel_exposure_policy_contract()

    metadata_map = {entry.panel_id: entry for entry in metadata_contract.entries}
    exposure_map = {entry.panel_id: entry for entry in exposure_contract.entries}

    display_titles: dict[str, str] = {
        "display_foundation_primary": "Foundation Primary Display",
        "display_foundation_secondary": "Foundation Secondary Display",
        "display_operator_interaction": "Operator Interaction Display",
    }

    entries = tuple(
        PanelBindingEntry(
            panel_id=panel_id,
            display_target_id=display_target_id,
            binding_reason=resolve_binding_reason(panel_id),
            is_default_target=True,
            eligible_for_main_dashboard=exposure_map[panel_id].visible_in_main_dashboard,
            eligible_for_oob_dashboard=exposure_map[panel_id].visible_in_oob_dashboard,
            description=(
                f"Canonical panel binding entry for {metadata_map[panel_id].title} "
                f"to {display_titles[display_target_id]}."
            ),
        )
        for panel_id in metadata_map
        for display_target_id in (resolve_display_target_id(panel_id),)
    )

    return PanelBindingContract(entries=entries)
