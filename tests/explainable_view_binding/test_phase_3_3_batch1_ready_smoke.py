from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_presentation_binding_contract,
    build_explainable_presentation_preview,
    build_explainable_presentation_summary,
)


def test_phase_3_3_batch1_ready_smoke() -> None:
    contract = build_explainable_presentation_binding_contract()
    summary = build_explainable_presentation_summary()
    preview = build_explainable_presentation_preview()

    assert contract.ready_bindings == contract.total_bindings
    assert contract.explainable_source_bound_bindings == contract.total_bindings
    assert contract.action_execution_allowed_bindings == 0
    assert contract.direct_display_switching_allowed_bindings == 0
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
