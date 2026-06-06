from __future__ import annotations

import MAKSIMAR_SERVER.WORKERS.simulation_worker.backend_selection_policy as backend_policy
from MAKSIMAR_CORE_LIB.node_roles.multi_gpu_profile_models import (
    MultiGpuProfile,
    MultiGpuProfileContract,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    build_simulation_engine_observability_contract,
)


def _build_no_gpu_profile_contract() -> MultiGpuProfileContract:
    nodes = tuple(
        MultiGpuProfile(node_id=node_id, gpu_count=0, accelerators=())
        for node_id in ("mobile_001", "dev_001", "home_001")
    )
    return MultiGpuProfileContract(total_nodes=len(nodes), nodes=nodes)


def test_simulation_engine_observability_binding_builds() -> None:
    contract = build_simulation_engine_observability_contract()

    assert contract.total_records == 2
    assert len(contract.records) == 2


def test_simulation_engine_observability_binding_contains_selected_backend() -> None:
    contract = build_simulation_engine_observability_contract()

    first = contract.records[0]
    assert first.task_id == "task_sim_obs_001"
    assert first.selected_backend in ("python", "fallback")

    if first.selected_backend == "python":
        assert first.execution_status == "completed"
        assert first.fallback_triggered is False
    else:
        assert first.execution_status == "fallback_routed"
        assert first.fallback_triggered is True


def test_simulation_engine_observability_binding_gpu_required_matches_current_hardware() -> None:
    contract = build_simulation_engine_observability_contract()

    second = contract.records[1]
    assert second.task_id == "task_sim_obs_002"
    assert second.selected_backend in ("python", "fallback")
    assert second.speech_chat_fast_path is True

    if second.selected_backend == "python":
        assert second.execution_status == "completed"
        assert second.fallback_triggered is False
    else:
        assert second.execution_status == "fallback_routed"
        assert second.fallback_triggered is True


def test_simulation_engine_observability_binding_contains_simulated_no_gpu_fallback_path(monkeypatch) -> None:
    monkeypatch.setattr(
        backend_policy,
        "build_multi_gpu_profile_contract",
        _build_no_gpu_profile_contract,
    )

    contract = build_simulation_engine_observability_contract()

    second = contract.records[1]
    assert second.task_id == "task_sim_obs_002"
    assert second.selected_backend == "fallback"
    assert second.execution_status == "fallback_routed"
    assert second.fallback_triggered is True
    assert second.speech_chat_fast_path is True
