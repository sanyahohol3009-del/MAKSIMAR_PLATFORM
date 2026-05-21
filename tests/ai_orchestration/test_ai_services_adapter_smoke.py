from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.AI_ORCHESTRATION.adapters.ai_services_adapter import (
    AIServicesAdapterReadModel,
    build_ai_services_adapter_read_model,
)


def test_ai_services_adapter_points_to_existing_services_only() -> None:
    adapter = build_ai_services_adapter_read_model()

    assert adapter.adapter_id == "ai_services_adapter_v1"
    assert adapter.target_surface == "AI_SERVICES"
    assert adapter.points_to_existing_service is True
    assert adapter.duplicates_service_logic is False
    assert adapter.model_runtime_execution_allowed is False
    assert adapter.runtime_mutation_allowed is False
    assert adapter.proposal_only is True
    assert adapter.dashboard_safe is True
    assert adapter.read_only is True


def test_ai_services_adapter_rejects_duplicate_service_logic() -> None:
    with pytest.raises(ValueError, match="duplicates_service_logic"):
        AIServicesAdapterReadModel(
            adapter_id="bad",
            target_surface="AI_SERVICES",
            existing_service_binding_ref="AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml",
            points_to_existing_service=True,
            duplicates_service_logic=True,
            model_runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_services_adapter_rejects_model_runtime_execution() -> None:
    with pytest.raises(ValueError, match="model_runtime_execution_allowed"):
        AIServicesAdapterReadModel(
            adapter_id="bad",
            target_surface="AI_SERVICES",
            existing_service_binding_ref="AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml",
            points_to_existing_service=True,
            duplicates_service_logic=False,
            model_runtime_execution_allowed=True,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
