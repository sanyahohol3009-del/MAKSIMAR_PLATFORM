from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_models import (
    ViewTargetingContract,
    ViewTargetingEntry,
)


def resolve_view_target_kind(panel_id: str) -> str:
    """Resolve canonical target kind for a panel."""
    if panel_id in {
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    }:
        return "foundation_view"

    if panel_id in {
        "action_queue",
        "approval_queue",
        "audit_timeline",
    }:
        return "interaction_view"

    raise ValueError(f"unsupported panel_id for view target kind: {panel_id}")


def resolve_view_scope(panel_id: str) -> str:
    """Resolve canonical view scope for a panel."""
    if panel_id in {
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    }:
        return "foundation"

    if panel_id in {
        "action_queue",
        "approval_queue",
        "audit_timeline",
    }:
        return "interaction"

    raise ValueError(f"unsupported panel_id for view scope: {panel_id}")


def build_view_targeting_contract() -> ViewTargetingContract:
    """Build the canonical view-targeting contract."""
    panel_binding_contract = build_panel_binding_contract()

    view_id_map: dict[str, str] = {
        "system_status": "view_foundation_status",
        "guard_chain": "view_foundation_status",
        "incidents": "view_foundation_status",
        "logs": "view_foundation_observability",
        "topology": "view_foundation_observability",
        "action_queue": "view_operator_interaction",
        "approval_queue": "view_operator_interaction",
        "audit_timeline": "view_operator_interaction",
    }

    entries = tuple(
        ViewTargetingEntry(
            panel_id=entry.panel_id,
            view_id=view_id_map[entry.panel_id],
            view_target_kind=resolve_view_target_kind(entry.panel_id),
            view_scope=resolve_view_scope(entry.panel_id),
            description=(
                f"Canonical view-targeting entry for {entry.panel_id}: "
                f"{view_id_map[entry.panel_id]}."
            ),
        )
        for entry in panel_binding_contract.entries
    )

    return ViewTargetingContract(entries=entries)
