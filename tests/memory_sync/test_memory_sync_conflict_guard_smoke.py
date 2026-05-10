from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_conflict_guard_contract


def test_memory_sync_conflict_guard_smoke() -> None:
    contract = build_memory_sync_conflict_guard_contract()

    assert contract.total_guards == 3
    assert contract.ready_guards == contract.total_guards
    assert contract.conflict_detection_required_guards == contract.total_guards
    assert contract.conflict_marker_required_guards == contract.total_guards
    assert contract.proposal_required_guards == contract.total_guards
    assert contract.human_approval_required_guards == contract.total_guards
    assert contract.rollback_reference_required_guards == contract.total_guards
    assert contract.auto_conflict_resolution_allowed_guards == 0
    assert contract.parallel_truth_allowed_guards == 0
    assert contract.canonical_write_allowed_guards == 0
    assert contract.client_canonical_write_allowed_guards == 0
    assert contract.runtime_mutation_allowed_guards == 0
