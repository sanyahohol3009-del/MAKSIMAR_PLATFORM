from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_request_contract,
)


def test_presentation_request_models_smoke() -> None:
    contract = build_presentation_request_contract()

    assert contract.total_requests == 3
    assert contract.ready_requests == contract.total_requests
    assert contract.explanation_required_requests == contract.total_requests
    assert contract.multilingual_ready_requests == contract.total_requests
    assert contract.read_only_requests == contract.total_requests
    assert contract.action_execution_allowed_requests == 0
    assert contract.direct_display_switching_allowed_requests == 0
