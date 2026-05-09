from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_conflict_marker_contract


def test_conflict_marker_models_smoke() -> None:
    contract = build_conflict_marker_contract()

    assert contract.total_markers == 6
    assert contract.conflict_detected_markers == 0
    assert contract.ready_markers == contract.total_markers
