from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


@dataclass(frozen=True, slots=True)
class PanelBindingEntry:
    """Canonical binding entry between a panel and display target semantics."""

    panel_id: str
    display_target_id: str
    binding_reason: str
    is_default_target: bool
    eligible_for_main_dashboard: bool
    eligible_for_oob_dashboard: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelBindingContract:
    """Canonical panel binding contract."""

    total_entries: int
    primary_operator_bindings: int
    diagnostics_bindings: int
    expansion_bindings: int
    default_target_bindings: int
    entries: tuple[PanelBindingEntry, ...]


def build_panel_binding_contract() -> PanelBindingContract:
    """Build canonical panel binding contract."""
    metadata_contract = build_panel_metadata_contract()
    exposure_contract = build_panel_exposure_policy_contract()
    display_contract = build_display_target_vocabulary_contract()

    metadata_map = {entry.panel_id: entry for entry in metadata_contract.entries}
    exposure_map = {entry.panel_id: entry for entry in exposure_contract.entries}
    display_targets = {entry.display_target_id: entry for entry in display_contract.entries}

    def resolve_display_target_id(panel_id: str) -> str:
        metadata_entry = metadata_map[panel_id]
        exposure_entry = exposure_map[panel_id]

        if exposure_entry.exposure_level == "hidden_internal":
            return "display_tertiary_expansion"

        if metadata_entry.panel_family == "foundation_status":
            return "display_secondary_diagnostics"

        if metadata_entry.panel_family in ("diagnostics", "read_only_monitoring"):
            return "display_secondary_diagnostics"

        if metadata_entry.panel_family in ("interaction", "control"):
            return "display_primary_operator"

        if metadata_entry.panel_family == "execution_observability":
            return "display_tertiary_expansion"

        if metadata_entry.panel_family == "navigation":
            return "display_tertiary_expansion"

        return "display_primary_operator"

    def resolve_binding_reason(panel_id: str) -> str:
        metadata_entry = metadata_map[panel_id]
        exposure_entry = exposure_map[panel_id]

        if exposure_entry.exposure_level == "hidden_internal":
            return "hidden_internal_binding"
        if metadata_entry.panel_family == "foundation_status":
            return "foundation_monitoring_binding"
        if metadata_entry.panel_family in ("diagnostics", "read_only_monitoring"):
            return "diagnostics_monitoring_binding"
        if metadata_entry.panel_family in ("interaction", "control"):
            return "operator_surface_binding"
        if metadata_entry.panel_family == "execution_observability":
            return "expansion_observability_binding"
        if metadata_entry.panel_family == "navigation":
            return "navigation_internal_binding"
        return "fallback_binding"

    entries = tuple(
        PanelBindingEntry(
            panel_id=panel_id,
            display_target_id=display_target_id,
            binding_reason=resolve_binding_reason(panel_id),
            is_default_target=True,
            eligible_for_main_dashboard=exposure_map[panel_id].visible_in_main_dashboard,
            eligible_for_oob_dashboard=exposure_map[panel_id].visible_in_oob_dashboard,
            description=(
                f"Canonical panel binding entry for {metadata_map[panel_id].display_title} "
                f"to {display_targets[display_target_id].display_title}."
            ),
        )
        for panel_id in metadata_map
        for display_target_id in (resolve_display_target_id(panel_id),)
    )

    return PanelBindingContract(
        total_entries=len(entries),
        primary_operator_bindings=sum(
            1 for entry in entries if entry.display_target_id == "display_primary_operator"
        ),
        diagnostics_bindings=sum(
            1 for entry in entries if entry.display_target_id == "display_secondary_diagnostics"
        ),
        expansion_bindings=sum(
            1 for entry in entries if entry.display_target_id == "display_tertiary_expansion"
        ),
        default_target_bindings=sum(1 for entry in entries if entry.is_default_target),
        entries=entries,
    )
