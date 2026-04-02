from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_delivery_readiness_contract import (
    build_visual_preview_delivery_readiness_contract,
)


def test_visual_preview_delivery_readiness_contract_builds() -> None:
    """Preview delivery readiness contract should build successfully."""
    contract = build_visual_preview_delivery_readiness_contract()

    assert contract.contract_id == "visual_preview_delivery_readiness_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_preview_delivery_readiness_contains_expected_entry() -> None:
    """Preview delivery readiness contract should contain canonical entry."""
    contract = build_visual_preview_delivery_readiness_contract()
    entry = contract.entries[0]

    assert entry.readiness_id == "visual_preview_delivery_readiness_001"
    assert (
        entry.first_viewable_preview_id
        == "visual_first_viewable_premium_preview_001"
    )
    assert entry.readiness_mode == "preview_delivery_readiness"
    assert entry.readiness_status == "delivery_ready"


def test_visual_preview_delivery_readiness_preserves_truth_bound_read_only_boundary() -> None:
    """Preview delivery readiness should preserve truth-bound read-only boundary."""
    contract = build_visual_preview_delivery_readiness_contract()
    entry = contract.entries[0]

    assert entry.operator_facing_ready is True
    assert entry.delivery_ready is True
    assert entry.truth_bound_delivery is True
    assert entry.read_only is True


def test_visual_preview_delivery_readiness_binds_expected_visual_targets() -> None:
    """Preview delivery readiness should bind expected visual targets."""
    contract = build_visual_preview_delivery_readiness_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
