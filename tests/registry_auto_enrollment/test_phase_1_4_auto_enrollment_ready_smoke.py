from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_summary,
    build_registry_auto_enrollment_phase_readiness,
)


def test_phase_1_4_auto_enrollment_ready_smoke() -> None:
    summary = build_auto_enrollment_summary()
    readiness = build_registry_auto_enrollment_phase_readiness()

    assert summary["summary_ready"] is True
    assert summary["dry_run"] is True
    assert readiness.phase_ready is True
    assert readiness.summary_entries == summary["total_entries"]
