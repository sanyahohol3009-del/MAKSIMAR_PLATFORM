from __future__ import annotations

from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    build_simulation_engine_observability_contract,
)


def test_simulation_engine_observability_binding_builds() -> None:
    """Simulation engine observability binding should build successfully."""
    contract = build_simulation_engine_observability_contract()

    assert contract.total_records == 2
    assert len(contract.records) == 2


def test_simulation_engine_observability_binding_contains_selected_backend() -> None:
    """Simulation engine observability binding should expose selected backend data."""
    contract = build_simulation_engine_observability_contract()

    first = contract.records[0]
    assert first.task_id == "task_sim_obs_001"
    assert first.selected_backend == "python"
    assert first.execution_status == "completed"
    assert first.fallback_triggered is False


def test_simulation_engine_observability_binding_contains_fallback_path() -> None:
    """Simulation engine observability binding should expose fallback path data."""
    contract = build_simulation_engine_observability_contract()

    second = contract.records[1]
    assert second.task_id == "task_sim_obs_002"
    assert second.selected_backend == "fallback"
    assert second.execution_status == "fallback_routed"
    assert second.fallback_triggered is True
    assert second.speech_chat_fast_path is True
