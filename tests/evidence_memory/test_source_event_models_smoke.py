from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_source_event_contract


def test_source_event_models_smoke() -> None:
    contract = build_source_event_contract()

    assert contract.total_events == 6
    assert contract.ready_events == contract.total_events
