from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import (
    build_regulatory_surface_inventory_preview,
)


def test_regulatory_surface_inventory_smoke() -> None:
    preview = build_regulatory_surface_inventory_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_surfaces"] == ()
    assert preview["closed_memory_roadmap_present"] is True
    assert preview["regulatory_models_present"] is True
    assert preview["jurisdiction_models_present"] is True
    assert preview["tenant_models_present"] is True
    assert preview["source_version_chain_present"] is True
    assert preview["memory_policy_present"] is True
    assert preview["routing_surfaces_present"] is True
