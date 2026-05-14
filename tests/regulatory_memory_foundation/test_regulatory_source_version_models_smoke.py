from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_source_version_registry


def test_regulatory_source_version_models_smoke() -> None:
    registry = build_regulatory_source_version_registry()

    assert registry.registry_ready is True
    assert len(registry.sources) >= 3
    assert registry.source_version_required is True
    assert registry.effective_date_required is True
    assert registry.jurisdiction_id_required is True
    assert registry.tenant_scope_id_required is True
    assert registry.precedence_required is True
    assert registry.canonical_truth_update_allowed is False
    assert registry.runtime_mutation_allowed is False
