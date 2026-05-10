from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import build_mempalace_preview


def test_mempalace_preview_builder_smoke() -> None:
    preview = build_mempalace_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["guard_validation_ready"] is True
    assert preview["adapter_surface_ready"] is True
    assert preview["external_backend_connected"] is False
    assert preview["vendor_acquisition_required"] is True
    assert preview["download_performed"] is False
    assert preview["real_backend_enabled"] is False
    assert preview["canonical_write_allowed"] == 0
    assert preview["runtime_mutation_allowed"] == 0
