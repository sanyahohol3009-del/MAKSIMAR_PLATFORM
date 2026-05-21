from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.AI_ORCHESTRATION.adapters.workers_adapter import (
    WorkersAdapterReadModel,
    build_workers_adapter_read_model,
)


def test_workers_adapter_points_to_existing_workers_only() -> None:
    adapter = build_workers_adapter_read_model()

    assert adapter.adapter_id == "workers_adapter_v1"
    assert adapter.target_surface == "MAKSIMAR_SERVER/WORKERS"
    assert adapter.points_to_existing_workers is True
    assert adapter.duplicates_worker_logic is False
    assert adapter.worker_runtime_execution_allowed is False
    assert adapter.runtime_mutation_allowed is False
    assert adapter.proposal_only is True
    assert adapter.dashboard_safe is True
    assert adapter.read_only is True


def test_workers_adapter_rejects_duplicate_worker_logic() -> None:
    with pytest.raises(ValueError, match="duplicates_worker_logic"):
        WorkersAdapterReadModel(
            adapter_id="bad",
            target_surface="MAKSIMAR_SERVER/WORKERS",
            existing_worker_binding_ref="AI_ORCHESTRATION/existing_bindings/worker_binding.yaml",
            points_to_existing_workers=True,
            duplicates_worker_logic=True,
            worker_runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_workers_adapter_rejects_worker_runtime_execution() -> None:
    with pytest.raises(ValueError, match="worker_runtime_execution_allowed"):
        WorkersAdapterReadModel(
            adapter_id="bad",
            target_surface="MAKSIMAR_SERVER/WORKERS",
            existing_worker_binding_ref="AI_ORCHESTRATION/existing_bindings/worker_binding.yaml",
            points_to_existing_workers=True,
            duplicates_worker_logic=False,
            worker_runtime_execution_allowed=True,
            runtime_mutation_allowed=False,
            proposal_only=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
