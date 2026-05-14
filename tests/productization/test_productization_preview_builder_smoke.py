from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_productization_preview


def test_productization_preview_builder_smoke() -> None:
    preview = build_productization_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_id"] == "PHASE 6.8"
    assert "no_hidden_autonomy_gate" in preview["preview_path"]
    assert preview["sale_ready_claim_allowed"] is True
    assert preview["roadmap_v5_1_closure_allowed_next"] is True
