from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_render_handoff_contract import (
    OperatorDashboardRenderHandoffEntry,
    build_operator_dashboard_render_handoff_contract,
)


def test_operator_dashboard_render_handoff_contract_builds() -> None:
    """Operator dashboard render-handoff contract should build successfully."""
    contract = build_operator_dashboard_render_handoff_contract()

    assert contract.contract_id == "operator_dashboard_render_handoff_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_render_handoff_contract_contains_expected_entry() -> None:
    """Operator dashboard render-handoff contract should contain expected canonical entry."""
    contract = build_operator_dashboard_render_handoff_contract()
    entry = contract.entries[0]

    assert entry.render_handoff_id == "operator_dashboard_render_handoff_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.render_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.render_handoff_state == "render_handoff_ready"
    assert entry.render_handoff_class == "main_operator_render_handoff"
    assert entry.screen_state_ready is True
    assert entry.renderer_registered is True
    assert entry.operator_visible is True


def test_operator_dashboard_render_handoff_entry_rejects_unregistered_renderer() -> None:
    """Operator dashboard render-handoff entries must keep renderer registration true."""
    with pytest.raises(ValueError, match="renderer_registered must remain true"):
        OperatorDashboardRenderHandoffEntry(
            render_handoff_id="operator_dashboard_render_handoff_invalid",
            dashboard_id="dashboard_main_operator_001",
            render_surface_id="render_surface_workspace_operator_main_001",
            render_handoff_state="render_handoff_ready",
            render_handoff_class="main_operator_render_handoff",
            screen_state_ready=True,
            renderer_registered=False,
            operator_visible=True,
            description="Invalid operator dashboard render-handoff entry.",
        )
