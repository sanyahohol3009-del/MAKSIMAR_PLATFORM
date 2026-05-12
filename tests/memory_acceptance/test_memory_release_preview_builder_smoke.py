from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_release_preview


def test_memory_release_preview_builder_smoke() -> None:
    preview = build_memory_release_preview()

    assert preview["release_preview_ready"] is True
    assert preview["memory_product_ready"] is True
    assert "phase_6_0_acceptance_gates" in preview["preview_path"]
    assert "phase_6_0_release_preview" in preview["preview_path"]
    assert preview["dashboard_read_only"] is True
