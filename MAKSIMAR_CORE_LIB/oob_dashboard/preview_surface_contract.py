from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_models import (
    PreviewSurfaceContract,
    PreviewSurfaceEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_composition_contract import (
    build_view_composition_contract,
)


def build_preview_surface_contract() -> PreviewSurfaceContract:
    """Build canonical preview surface contract."""
    panel_metadata_contract = build_panel_metadata_contract()
    panel_exposure_contract = build_panel_exposure_policy_contract()
    view_composition_contract = build_view_composition_contract()
    interaction_surface_contract = build_main_operator_interaction_surface_contract()

    exposure_by_panel = {
        entry.panel_id: entry for entry in panel_exposure_contract.entries
    }

    if not view_composition_contract.entries:
        raise ValueError("view composition contract must expose at least one entry.")

    foundation_workspace_id = view_composition_contract.entries[0].workspace_id

    interaction_workspace_ids = {
        entry.workspace_id for entry in interaction_surface_contract.entries
    }
    if not interaction_workspace_ids:
        raise ValueError(
            "main operator interaction surface contract must expose at least one workspace."
        )
    interaction_workspace_id = sorted(interaction_workspace_ids)[0]

    interaction_panel_ids = {
        "action_queue",
        "approval_queue",
        "audit_timeline",
    }

    entries = tuple(
        PreviewSurfaceEntry(
            preview_surface_id=f"preview_surface_{index:03d}",
            panel_id=entry.panel_id,
            workspace_id=(
                interaction_workspace_id
                if entry.panel_id in interaction_panel_ids
                else foundation_workspace_id
            ),
            preview_surface_state="preview_surface_ready",
            preview_surface_class=(
                "interaction_preview_surface"
                if entry.panel_id in interaction_panel_ids
                else "foundation_preview_surface"
            ),
            preview_generation_mode=(
                "fixture_preview_generation"
                if entry.panel_id in interaction_panel_ids
                else "panel_preview_generation"
            ),
            visible_in_navigation=exposure_by_panel[entry.panel_id].visible_in_navigation,
            visible_in_main_dashboard=exposure_by_panel[
                entry.panel_id
            ].visible_in_main_dashboard,
            operator_visible=entry.operator_visible,
            description=(
                f"Canonical preview surface entry for panel {entry.panel_id}."
            ),
        )
        for index, entry in enumerate(panel_metadata_contract.entries, start=1)
    )

    return PreviewSurfaceContract(
        contract_id="preview_surface_contract_001",
        total_entries=len(entries),
        foundation_preview_entries=sum(
            1
            for entry in entries
            if entry.preview_surface_class == "foundation_preview_surface"
        ),
        interaction_preview_entries=sum(
            1
            for entry in entries
            if entry.preview_surface_class == "interaction_preview_surface"
        ),
        panel_preview_generation_entries=sum(
            1
            for entry in entries
            if entry.preview_generation_mode == "panel_preview_generation"
        ),
        fixture_preview_generation_entries=sum(
            1
            for entry in entries
            if entry.preview_generation_mode == "fixture_preview_generation"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
