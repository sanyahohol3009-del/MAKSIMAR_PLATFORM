from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_memory_summary,
)


def test_enterprise_memory_summary_builder_smoke() -> None:
    summary = build_enterprise_memory_summary()

    assert summary["summary_ready"] is True
    assert summary["tenant_scopes"] == 3
    assert summary["legal_jurisdictions"] == 3
    assert summary["regulatory_records"] == 3
    assert summary["memory_isolations"] == 3
    assert summary["enterprise_policy_records"] == 3
    assert summary["customer_metrics_records"] == 3
    assert summary["runtime_policy_binding_allowed"] == 0
    assert summary["cross_boundary_merge_allowed"] == 0
    assert summary["pii_exposure_allowed_metrics"] == 0
