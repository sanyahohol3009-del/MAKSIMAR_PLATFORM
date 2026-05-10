from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_memory_preview,
)


def test_enterprise_memory_preview_builder_smoke() -> None:
    preview = build_enterprise_memory_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["tenant_scopes"] == 3
    assert preview["regulatory_records"] == 3
    assert preview["enterprise_policy_records"] == 3
    assert preview["customer_metrics_records"] == 3
    assert preview["country_codes"] == ("DE", "UA", "EU")
    assert preview["runtime_policy_binding_allowed"] == 0
    assert preview["cross_boundary_merge_allowed"] == 0
