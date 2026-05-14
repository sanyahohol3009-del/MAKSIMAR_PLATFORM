from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_next_roadmap_entrypoint_preview


def test_next_roadmap_entrypoint_smoke() -> None:
    preview = build_next_roadmap_entrypoint_preview()

    assert preview["preview_ready"] is True
    assert preview["recommended_first"] == "multi_tenant_multi_country_regulatory_memory_track"
    assert "visual_operator_dashboard_track" in preview["candidates"]
    assert "network_security_deployment_boundary_track" in preview["candidates"]
