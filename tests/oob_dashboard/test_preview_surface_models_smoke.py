from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_models import (
    PreviewSurfaceContract,
    PreviewSurfaceEntry,
)


def test_preview_surface_entry_builds() -> None:
    """Preview surface entry should build successfully."""
    entry = PreviewSurfaceEntry(
        preview_surface_id="preview_surface_001",
        panel_id="system_status",
        workspace_id="workspace_foundation_monitoring",
        preview_surface_state="preview_surface_ready",
        preview_surface_class="foundation_preview_surface",
        preview_generation_mode="panel_preview_generation",
        visible_in_navigation=True,
        visible_in_main_dashboard=True,
        operator_visible=True,
        description="Canonical preview surface entry.",
    )

    assert entry.preview_surface_id == "preview_surface_001"
    assert entry.preview_surface_state == "preview_surface_ready"
    assert entry.preview_surface_class == "foundation_preview_surface"
    assert entry.preview_generation_mode == "panel_preview_generation"


def test_preview_surface_entry_rejects_non_navigation_visible() -> None:
    """Preview surface entry must remain navigation-visible."""
    with pytest.raises(
        ValueError,
        match="visible_in_navigation must remain true for canonical preview surfaces.",
    ):
        PreviewSurfaceEntry(
            preview_surface_id="preview_surface_invalid",
            panel_id="system_status",
            workspace_id="workspace_foundation_monitoring",
            preview_surface_state="preview_surface_ready",
            preview_surface_class="foundation_preview_surface",
            preview_generation_mode="panel_preview_generation",
            visible_in_navigation=False,
            visible_in_main_dashboard=True,
            operator_visible=True,
            description="Invalid preview surface entry.",
        )


def test_preview_surface_contract_builds() -> None:
    """Preview surface contract should build successfully."""
    entries = (
        PreviewSurfaceEntry(
            preview_surface_id="preview_surface_001",
            panel_id="system_status",
            workspace_id="workspace_foundation_monitoring",
            preview_surface_state="preview_surface_ready",
            preview_surface_class="foundation_preview_surface",
            preview_generation_mode="panel_preview_generation",
            visible_in_navigation=True,
            visible_in_main_dashboard=True,
            operator_visible=True,
            description="Foundation preview entry.",
        ),
        PreviewSurfaceEntry(
            preview_surface_id="preview_surface_002",
            panel_id="action_queue",
            workspace_id="workspace_operator_interaction",
            preview_surface_state="preview_surface_ready",
            preview_surface_class="interaction_preview_surface",
            preview_generation_mode="fixture_preview_generation",
            visible_in_navigation=True,
            visible_in_main_dashboard=True,
            operator_visible=True,
            description="Interaction preview entry.",
        ),
    )

    contract = PreviewSurfaceContract(
        contract_id="preview_surface_contract_001",
        total_entries=2,
        foundation_preview_entries=1,
        interaction_preview_entries=1,
        panel_preview_generation_entries=1,
        fixture_preview_generation_entries=1,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.foundation_preview_entries == 1
    assert contract.interaction_preview_entries == 1
