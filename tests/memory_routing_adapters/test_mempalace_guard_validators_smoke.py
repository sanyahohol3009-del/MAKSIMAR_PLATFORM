from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_guard_validation_report,
)


def test_mempalace_guard_validators_smoke() -> None:
    report = build_mempalace_guard_validation_report()

    assert report.guard_validation_ready is True
    assert report.allowed_domains_ready is True
    assert report.forbidden_domains_absent is True
    assert report.no_source_of_truth is True
    assert report.no_canonical_truth is True
    assert report.no_regulatory_memory is True
    assert report.no_enterprise_policy_memory is True
    assert report.no_technical_truth is True
    assert report.no_audit_truth is True
    assert report.no_approval_truth is True
    assert report.no_canonical_write is True
    assert report.no_auto_promotion is True
    assert report.no_auto_conflict_resolution is True
    assert report.no_runtime_mutation is True
