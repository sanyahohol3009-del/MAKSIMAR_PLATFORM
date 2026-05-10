from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_memory_phase_preview,
    build_enterprise_memory_preview,
)


def test_phase_4_1_visible_preview_smoke() -> None:
    preview = build_enterprise_memory_preview()
    phase_preview = build_enterprise_memory_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["runtime_policy_binding_allowed"] == 0
    assert preview["cross_boundary_merge_allowed"] == 0
    assert preview["pii_exposure_allowed_metrics"] == 0

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["no_runtime_policy_binding"] is True
    assert phase_preview["no_cross_boundary_merge"] is True
    assert phase_preview["no_pii_exposure"] is True
