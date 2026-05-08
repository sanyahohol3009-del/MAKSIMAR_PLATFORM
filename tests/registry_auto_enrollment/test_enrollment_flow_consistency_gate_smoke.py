from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_phase_readiness,
)


def test_enrollment_flow_consistency_gate_smoke() -> None:
    readiness = build_registry_auto_enrollment_phase_readiness()

    assert readiness.flow == (
        "manifest_discovery",
        "candidate_builder",
        "write_guard",
        "dry_run_runner",
        "registry_entry_ready",
        "dashboard_exposure_ready",
        "observability_binding_ready",
    )
    assert readiness.flow_consistent is True
