from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_guard_validation_report,
    build_mempalace_preview,
)


def test_phase_5_1_no_canonical_truth_smoke() -> None:
    guards = build_mempalace_guard_validation_report()
    preview = build_mempalace_preview()

    assert guards.no_source_of_truth is True
    assert guards.no_canonical_truth is True
    assert guards.no_regulatory_memory is True
    assert guards.no_enterprise_policy_memory is True
    assert guards.no_technical_truth is True
    assert guards.no_audit_truth is True
    assert guards.no_approval_truth is True

    assert preview["source_of_truth_adapters"] == 0
    assert preview["canonical_truth_allowed_capabilities"] == 0
    assert preview["regulatory_memory_allowed_capabilities"] == 0
    assert preview["enterprise_policy_memory_allowed_capabilities"] == 0
    assert preview["technical_truth_allowed_capabilities"] == 0
    assert preview["audit_truth_allowed_capabilities"] == 0
    assert preview["approval_truth_allowed_capabilities"] == 0
