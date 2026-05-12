from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.governance_federation_gap_report_builder import (
    REQUIRED_EXISTING_SURFACES,
    build_governance_federation_gap_report,
)


def test_governance_reuses_existing_surfaces_smoke() -> None:
    report = build_governance_federation_gap_report()

    assert len(REQUIRED_EXISTING_SURFACES) >= 10
    assert report["existing_surfaces_reused"] is True
    assert report["missing_required_surfaces"] == ()
