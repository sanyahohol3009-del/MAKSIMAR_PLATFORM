from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_adapter_selection_metrics_contract,
)


def test_memory_adapter_selection_metrics_models_smoke() -> None:
    contract = build_memory_adapter_selection_metrics_contract()

    assert contract.total_entries == 2
    assert contract.ready_entries == contract.total_entries
    assert contract.backend_execution_allowed_entries == 0
    assert contract.policy_gate_ready_entries == contract.total_entries
    assert contract.mgrep_blocked_entries == contract.total_entries
    assert contract.sqlite_vec_blocked_entries == contract.total_entries
    assert contract.read_only_entries == contract.total_entries
