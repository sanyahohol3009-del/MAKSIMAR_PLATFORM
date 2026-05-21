from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.ai_router_binding_contract import (
    AIRouterBindingContract,
    build_ai_router_binding_contract,
)


def test_ai_router_binding_contract_accounts_existing_router_only() -> None:
    contract = build_ai_router_binding_contract()

    assert contract.contract_id == "ai_orchestration_ai_router_binding_accounting_v1"
    assert contract.accounts_existing_router_binding is True
    assert contract.duplicates_control_plane_router is False
    assert contract.replaces_control_plane_router is False
    assert contract.route_execution_allowed is False
    assert contract.direct_model_execution_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True


def test_ai_router_binding_contract_rejects_router_duplication() -> None:
    with pytest.raises(ValueError, match="duplicates_control_plane_router"):
        AIRouterBindingContract(
            contract_id="bad",
            existing_control_plane_router_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            existing_ai_orchestration_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
            existing_runtime_adapter_ref="MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py",
            accounts_existing_router_binding=True,
            duplicates_control_plane_router=True,
            replaces_control_plane_router=False,
            route_execution_allowed=False,
            direct_model_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_router_binding_contract_rejects_router_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_control_plane_router"):
        AIRouterBindingContract(
            contract_id="bad",
            existing_control_plane_router_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            existing_ai_orchestration_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
            existing_runtime_adapter_ref="MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py",
            accounts_existing_router_binding=True,
            duplicates_control_plane_router=False,
            replaces_control_plane_router=True,
            route_execution_allowed=False,
            direct_model_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_router_binding_contract_rejects_route_execution() -> None:
    with pytest.raises(ValueError, match="route_execution_allowed"):
        AIRouterBindingContract(
            contract_id="bad",
            existing_control_plane_router_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            existing_ai_orchestration_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
            existing_runtime_adapter_ref="MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py",
            accounts_existing_router_binding=True,
            duplicates_control_plane_router=False,
            replaces_control_plane_router=False,
            route_execution_allowed=True,
            direct_model_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
