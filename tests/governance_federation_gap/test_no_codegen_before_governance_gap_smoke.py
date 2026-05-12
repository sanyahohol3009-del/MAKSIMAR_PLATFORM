from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.governance_federation_gap_report_builder import (
    build_governance_federation_gap_report,
)


def test_no_codegen_before_governance_gap_smoke() -> None:
    report = build_governance_federation_gap_report()

    assert report["proposal_audit_allowed_next"] is True
    assert report["codegen_allowed_now"] is False
    assert report["sandbox_allowed_now"] is False
    assert report["self_expansion_allowed_now"] is False
