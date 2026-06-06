from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.workers_registry.worker_alias_binding_contract import (
    CANONICAL_WORKER_IDS,
    WorkerAliasBinding,
    WorkerAliasBindingContract,
    build_worker_alias_binding_contract,
    resolve_worker_alias,
)
from MAKSIMAR_CORE_LIB.workers_registry.worker_role_binding_contract import (
    JARVIS_LIVE_WORKER_ROLES,
    WorkerRoleBinding,
    build_worker_role_binding_contract,
)


def test_worker_roles_are_bound_to_existing_worker_registry() -> None:
    contract = build_worker_role_binding_contract()
    read_model = contract.to_read_model()

    assert tuple(read_model["roles"]) == JARVIS_LIVE_WORKER_ROLES
    assert read_model["canonical_worker_ids"] == (
        "worker_ai_001",
        "worker_sim_001",
        "worker_voice_001",
    )
    assert read_model["reused_existing_worker_registry"] is True
    assert read_model["new_worker_registry_created"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["shell_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False


def test_worker_alias_resolves_simulation_analysis_drift() -> None:
    contract = build_worker_alias_binding_contract()

    assert contract.canonical_worker_ids == CANONICAL_WORKER_IDS
    assert resolve_worker_alias("worker_simulation_analysis_001") == "worker_sim_001"
    assert contract.resolve_worker_id("worker_sim_001") == "worker_sim_001"


def test_unknown_canonical_worker_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown canonical worker id"):
        WorkerAliasBindingContract(
            canonical_worker_ids=CANONICAL_WORKER_IDS,
            alias_bindings=(
                WorkerAliasBinding("worker_unknown_alias_001", "worker_missing_001"),
            ),
        )


def test_invalid_alias_loop_is_rejected() -> None:
    with pytest.raises(ValueError, match="alias loop"):
        WorkerAliasBindingContract(
            canonical_worker_ids=CANONICAL_WORKER_IDS,
            alias_bindings=(
                WorkerAliasBinding("worker_loop_a_001", "worker_loop_b_001"),
                WorkerAliasBinding("worker_loop_b_001", "worker_loop_a_001"),
            ),
        )


def test_self_alias_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not point to itself"):
        WorkerAliasBinding("worker_sim_001", "worker_sim_001")


def test_dataclasses_validate_through_post_init() -> None:
    with pytest.raises(ValueError, match="unsupported value"):
        WorkerRoleBinding(
            role="unknown_role",
            canonical_worker_id="worker_ai_001",
            source_surface="MAKSIMAR_CORE_LIB/workers_registry",
        )

    with pytest.raises(ValueError, match="must remain disabled"):
        WorkerRoleBinding(
            role="model_chat",
            canonical_worker_id="worker_ai_001",
            source_surface="MAKSIMAR_CORE_LIB/workers_registry",
            runtime_start_allowed=True,
        )

