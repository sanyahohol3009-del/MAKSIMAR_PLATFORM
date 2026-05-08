from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_dry_run_result,
    build_auto_enrollment_summary,
    build_enrollment_candidate_contract,
    build_manifest_discovery_contract,
)


def test_auto_enrollment_ready_smoke() -> None:
    discovery = build_manifest_discovery_contract()
    candidates = build_enrollment_candidate_contract(discovery=discovery)
    result = build_auto_enrollment_dry_run_result(candidates=candidates)
    summary = build_auto_enrollment_summary(dry_run_result=result)

    assert discovery.total_entries == candidates.total_candidates
    assert candidates.total_candidates == result.total_entries
    assert result.total_entries == summary["total_entries"]
    assert summary["summary_ready"] is True
