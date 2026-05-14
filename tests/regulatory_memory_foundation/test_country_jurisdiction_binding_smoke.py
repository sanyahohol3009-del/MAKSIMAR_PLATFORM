from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_country_jurisdiction_binding_preview


def test_country_jurisdiction_binding_smoke() -> None:
    preview = build_country_jurisdiction_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_surfaces"] == ()
    assert "DE" in preview["country_codes"]
    assert "EU" in preview["country_codes"]
    assert preview["step_1_ready"] is True
    assert preview["registry_ready"] is True
    assert preview["no_cross_jurisdiction_merge"] is True
