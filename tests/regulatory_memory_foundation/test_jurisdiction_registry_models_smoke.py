from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_jurisdiction_registry


def test_jurisdiction_registry_models_smoke() -> None:
    registry = build_jurisdiction_registry()

    assert registry.registry_ready is True
    assert len(registry.entries) >= 5
    assert registry.country_code_required is True
    assert registry.jurisdiction_id_required is True
    assert registry.applicability_scope_required is True
    assert registry.source_bound_required is True
    assert registry.cross_jurisdiction_merge_allowed is False
