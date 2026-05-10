from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_phase_readiness,
    build_presentation_preview,
    build_presentation_router_contract,
    build_presentation_summary,
)


def test_phase_3_2_no_direct_switching_smoke() -> None:
    router = build_presentation_router_contract()
    summary = build_presentation_summary()
    preview = build_presentation_preview()
    readiness = build_presentation_phase_readiness()

    assert router.direct_display_switching_allowed_routes == 0
    assert summary["display_target_direct_switching_allowed"] == 0
    assert summary["presentation_direct_display_switching_allowed_routes"] == 0
    assert preview["direct_display_switching_allowed"] == 0
    assert readiness.direct_display_switching_allowed == 0
