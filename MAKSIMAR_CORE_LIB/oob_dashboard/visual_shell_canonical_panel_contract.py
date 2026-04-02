from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_integration_contract import (
    build_display_runtime_resolver_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    normalize_panel_id,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_contract import (
    build_view_targeting_contract,
)


@dataclass(frozen=True, slots=True)
class VisualShellCanonicalPanelEntry:
    """Canonical visual-shell panel entry."""

    panel_id: str
    present_in_main_operator_dashboard: bool
    present_in_main_operator_read_model: bool
    present_in_panel_binding: bool
    present_in_view_targeting: bool
    present_in_panel_view_display_chain: bool
    present_in_display_runtime_resolver: bool
    canonical_panel_id_only: bool
    visual_shell_allowed: bool


@dataclass(frozen=True, slots=True)
class VisualShellCanonicalPanelContract:
    """Canonical panel contract for the visual shell boundary."""

    contract_id: str
    total_entries: int
    canonical_only_entries: int
    visual_shell_allowed_entries: int
    legacy_alias_entries: int
    entries: tuple[VisualShellCanonicalPanelEntry, ...]


def _collect_main_operator_panel_ids() -> tuple[set[str], set[str]]:
    """Collect canonical panel ids reachable from main operator dashboard layers."""
    layout_contract = build_layout_composition_contract()
    main_operator_dashboard = build_main_operator_dashboard_contract()
    main_operator_read_model = build_main_operator_dashboard_read_model_contract()

    dashboard_workspace_ids = {
        entry.workspace_id for entry in main_operator_dashboard.entries
    }
    read_model_workspace_ids = {
        entry.workspace_id for entry in main_operator_read_model.entries
    }

    dashboard_panel_ids = {
        entry.panel_id
        for entry in layout_contract.entries
        if entry.workspace_id in dashboard_workspace_ids
    }
    read_model_panel_ids = {
        entry.panel_id
        for entry in layout_contract.entries
        if entry.workspace_id in read_model_workspace_ids
    }

    return dashboard_panel_ids, read_model_panel_ids


def _collect_panel_ids() -> dict[str, set[str]]:
    """Collect panel ids from all visual-shell upstream contracts."""
    (
        main_operator_dashboard_panel_ids,
        main_operator_read_model_panel_ids,
    ) = _collect_main_operator_panel_ids()
    panel_binding = build_panel_binding_contract()
    view_targeting = build_view_targeting_contract()
    panel_view_display_chain = build_panel_view_display_chain_contract()
    display_runtime_resolver = build_display_runtime_resolver_integration_contract()

    return {
        "main_operator_dashboard": main_operator_dashboard_panel_ids,
        "main_operator_read_model": main_operator_read_model_panel_ids,
        "panel_binding": {
            entry.panel_id for entry in panel_binding.entries
        },
        "view_targeting": {
            entry.panel_id for entry in view_targeting.entries
        },
        "panel_view_display_chain": {
            entry.panel_id for entry in panel_view_display_chain.entries
        },
        "display_runtime_resolver": {
            entry.panel_id for entry in display_runtime_resolver.entries
        },
    }


def build_visual_shell_canonical_panel_contract() -> (
    VisualShellCanonicalPanelContract
):
    """Build canonical visual-shell panel contract."""
    panel_sources = _collect_panel_ids()

    all_panel_ids = sorted(
        {
            panel_id
            for panel_ids in panel_sources.values()
            for panel_id in panel_ids
        }
    )

    entries = tuple(
        VisualShellCanonicalPanelEntry(
            panel_id=panel_id,
            present_in_main_operator_dashboard=(
                panel_id in panel_sources["main_operator_dashboard"]
            ),
            present_in_main_operator_read_model=(
                panel_id in panel_sources["main_operator_read_model"]
            ),
            present_in_panel_binding=(
                panel_id in panel_sources["panel_binding"]
            ),
            present_in_view_targeting=(
                panel_id in panel_sources["view_targeting"]
            ),
            present_in_panel_view_display_chain=(
                panel_id in panel_sources["panel_view_display_chain"]
            ),
            present_in_display_runtime_resolver=(
                panel_id in panel_sources["display_runtime_resolver"]
            ),
            canonical_panel_id_only=(normalize_panel_id(panel_id) == panel_id),
            visual_shell_allowed=(normalize_panel_id(panel_id) == panel_id),
        )
        for panel_id in all_panel_ids
    )

    return VisualShellCanonicalPanelContract(
        contract_id="visual_shell_canonical_panel_contract_001",
        total_entries=len(entries),
        canonical_only_entries=sum(
            1 for entry in entries if entry.canonical_panel_id_only
        ),
        visual_shell_allowed_entries=sum(
            1 for entry in entries if entry.visual_shell_allowed
        ),
        legacy_alias_entries=sum(
            1 for entry in entries if not entry.canonical_panel_id_only
        ),
        entries=entries,
    )
