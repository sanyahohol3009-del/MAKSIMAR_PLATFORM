from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import build_mempalace_adapter_surface


def test_mempalace_adapter_surface_smoke() -> None:
    surface = build_mempalace_adapter_surface()

    assert surface.adapter_surface_ready is True
    assert surface.query_only_surface_ready is True
    assert surface.external_backend_connected is False
    assert surface.vendor_acquisition_required is True
    assert surface.download_performed is False
    assert surface.real_backend_enabled is False
    assert surface.canonical_write_allowed is False
    assert surface.runtime_mutation_allowed is False
