from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_conflict_guard_contract,
    build_memory_sync_phase_readiness,
)


def test_phase_4_3_conflict_guard_required_smoke() -> None:
    guards = build_memory_sync_conflict_guard_contract()
    readiness = build_memory_sync_phase_readiness()

    assert guards.conflict_detection_required_guards == guards.total_guards
    assert guards.conflict_marker_required_guards == guards.total_guards
    assert guards.proposal_required_guards == guards.total_guards
    assert guards.human_approval_required_guards == guards.total_guards
    assert guards.rollback_reference_required_guards == guards.total_guards
    assert readiness.conflict_guard_ready is True
