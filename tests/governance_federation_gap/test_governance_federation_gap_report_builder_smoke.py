from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.governance_federation_gap_report_builder import (
    build_governance_federation_gap_report,
)


def test_governance_federation_gap_report_builder_smoke() -> None:
    report = build_governance_federation_gap_report()

    assert report["gap_pass_ready"] is True
    assert report["existing_surfaces_reused"] is True
    assert report["missing_required_surfaces"] == ()
    assert report["trust_scope_ready"] is True
    assert report["source_priority_ready"] is True
    assert report["federation_policy_ready"] is True
    assert report["tenant_personal_separation_ready"] is True
