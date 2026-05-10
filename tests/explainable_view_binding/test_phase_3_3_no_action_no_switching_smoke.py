from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_phase_readiness,
    build_explainable_presentation_binding_contract,
    build_explainable_presentation_preview,
    build_explainable_presentation_summary,
)


def test_phase_3_3_no_action_no_switching_smoke() -> None:
    contract = build_explainable_presentation_binding_contract()
    summary = build_explainable_presentation_summary()
    preview = build_explainable_presentation_preview()
    readiness = build_explainable_phase_readiness()

    assert contract.action_execution_allowed_bindings == 0
    assert contract.direct_display_switching_allowed_bindings == 0
    assert summary["action_execution_allowed_bindings"] == 0
    assert summary["direct_display_switching_allowed_bindings"] == 0
    assert preview["action_execution_allowed_bindings"] == 0
    assert preview["direct_display_switching_allowed_bindings"] == 0
    assert readiness.action_execution_allowed == 0
    assert readiness.direct_display_switching_allowed == 0
