from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_phase_readiness,
)


def test_enrollment_phase_readiness_gate_smoke() -> None:
    readiness = build_registry_auto_enrollment_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.counts_consistent is True
    assert readiness.flow_consistent is True
    assert readiness.no_write_verified is True
    assert readiness.write_guard_ready is True
    assert readiness.discovery_entries == readiness.candidate_entries
    assert readiness.candidate_entries == readiness.dry_run_entries
    assert readiness.dry_run_entries == readiness.summary_entries
