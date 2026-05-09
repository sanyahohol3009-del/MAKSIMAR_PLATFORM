from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_domain_layer_binding_contract,
    build_skill_domain_preview,
)


def test_layers_visible_smoke() -> None:
    layers = build_domain_layer_binding_contract()
    preview = build_skill_domain_preview()

    assert layers.total_layers == 6
    assert layers.ready_layers == layers.total_layers
    assert layers.source_exists_layers == layers.total_layers
    assert layers.registry_backed_layers == layers.total_layers
    assert layers.dashboard_visible_layers == layers.total_layers
    assert layers.read_only_layers == layers.total_layers

    layer_kinds = tuple(entry.layer_kind for entry in layers.entries)

    assert "skill_adapter_registry" in layer_kinds
    assert "domain_cubes" in layer_kinds
    assert "memory_registry" in layer_kinds
    assert "retrieval_orchestration" in layer_kinds
    assert "dashboard_read_only_views" in layer_kinds
    assert "architecture_map_runtime" in layer_kinds

    assert preview["domain_layers"] == 6
    assert preview["domain_layers_ready"] == 6
    assert preview["domain_layers_dashboard_visible"] == 6
    assert preview["domain_layers_read_only"] == 6
