from __future__ import annotations

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    build_ai_orchestration_acceptance_read_model,
    build_ai_router_binding_contract,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ai_orchestration_read_model_builder import (
    build_ai_orchestration_runtime_read_model,
)


def test_ai_orchestration_accounts_existing_surfaces_without_duplication() -> None:
    acceptance = build_ai_orchestration_acceptance_read_model()
    router_binding = build_ai_router_binding_contract()
    runtime = build_ai_orchestration_runtime_read_model()

    assert acceptance.ai_services_accounted is True
    assert acceptance.workers_accounted is True
    assert acceptance.ai_router_binding_accounted is True

    assert runtime.ai_services_adapter.points_to_existing_service is True
    assert runtime.ai_services_adapter.duplicates_service_logic is False

    assert runtime.workers_adapter.points_to_existing_workers is True
    assert runtime.workers_adapter.duplicates_worker_logic is False

    assert runtime.control_plane_router_adapter.points_to_existing_router_binding is True
    assert runtime.control_plane_router_adapter.duplicates_router_logic is False

    assert router_binding.accounts_existing_router_binding is True
    assert router_binding.duplicates_control_plane_router is False
    assert router_binding.replaces_control_plane_router is False


def test_ai_orchestration_final_acceptance_blocks_direct_execution_paths() -> None:
    acceptance = build_ai_orchestration_acceptance_read_model()
    runtime = build_ai_orchestration_runtime_read_model()

    assert acceptance.proposal_only is True
    assert acceptance.direct_execution_blocked is True
    assert acceptance.action_library_direct_execution_allowed is False
    assert acceptance.workflow_engine_direct_execution_allowed is False
    assert acceptance.runtime_mutation_allowed is False

    assert runtime.proposal_only is True
    assert runtime.runtime_mutation_allowed is False
    assert runtime.deployment_allowed is False
    assert runtime.public_exposure_allowed is False
