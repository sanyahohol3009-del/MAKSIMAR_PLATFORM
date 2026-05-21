from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.AI_ORCHESTRATION.adapters.control_plane_ai_router_adapter import (
    ControlPlaneAIRouterAdapterReadModel,
    build_control_plane_ai_router_adapter_read_model,
)


def test_control_plane_ai_router_adapter_points_to_existing_router_binding_only() -> None:
    adapter = build_control_plane_ai_router_adapter_read_model()

    assert adapter.adapter_id == "control_plane_ai_router_adapter_v1"
    assert adapter.target_surface == "CONTROL_PLANE/ai_router_binding"
    assert adapter.points_to_existing_router_binding is True
    assert adapter.duplicates_router_logic is False
    assert adapter.route_execution_allowed is False
    assert adapter.runtime_mutation_allowed is False
    assert adapter.proposal_only is True
    assert adapter.dashboard_safe is True
    assert adapter.read_only is True


def test_control_plane_ai_router_adapter_rejects_duplicate_router_logic() -> None:
    with pytest.raises(ValueError, match="duplicates_router_logic"):
        ControlPlaneAIRouterAdapterReadModel(
            adapter_id="bad",
            target_surface="CONTROL_PLANE/ai_router_binding",
            existing_router_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
            points_to_existing_router_binding=True,
            duplicates_router_logic=True,
            route_execution_allowed=False,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_control_plane_ai_router_adapter_rejects_route_execution() -> None:
    with pytest.raises(ValueError, match="route_execution_allowed"):
        ControlPlaneAIRouterAdapterReadModel(
            adapter_id="bad",
            target_surface="CONTROL_PLANE/ai_router_binding",
            existing_router_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
            points_to_existing_router_binding=True,
            duplicates_router_logic=False,
            route_execution_allowed=True,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
