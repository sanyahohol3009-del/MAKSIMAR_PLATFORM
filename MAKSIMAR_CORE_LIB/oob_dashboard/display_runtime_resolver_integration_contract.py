from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_models import (
    DisplayRuntimeResolverContract,
    DisplayRuntimeResolverEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


def resolve_fallback_display_target_id(display_target_id: str) -> str:
    """Resolve the canonical fallback display target."""
    fallback_map: dict[str, str] = {
        "display_foundation_primary": "display_foundation_secondary",
        "display_foundation_secondary": "display_foundation_primary",
        "display_operator_interaction": "display_operator_interaction",
    }

    if display_target_id not in fallback_map:
        raise ValueError(f"unsupported display_target_id for fallback: {display_target_id}")

    return fallback_map[display_target_id]


def build_display_runtime_resolver_integration_contract() -> DisplayRuntimeResolverContract:
    """Build the canonical display runtime resolver integration contract."""
    chain_contract = build_panel_view_display_chain_contract()

    entries = tuple(
        DisplayRuntimeResolverEntry(
            panel_id=entry.panel_id,
            view_id=entry.view_id,
            display_target_id=entry.display_target_id,
            resolved_display_role=entry.display_role,
            resolved_display_zone=entry.display_zone,
            fallback_display_target_id=resolve_fallback_display_target_id(
                entry.display_target_id
            ),
            description=(
                f"Canonical resolver integration entry for {entry.panel_id}: "
                f"{entry.display_target_id} -> fallback "
                f"{resolve_fallback_display_target_id(entry.display_target_id)}."
            ),
        )
        for entry in chain_contract.entries
    )

    return DisplayRuntimeResolverContract(entries=entries)
