from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_language_bridge_contract


def test_language_bridge_models_smoke() -> None:
    contract = build_language_bridge_contract()

    assert contract.language_bridge_models_ready is True
    assert contract.artifact_language_contract_ready is True
    assert len(contract.bridges) >= 3
    assert contract.build_test_required is True
    assert contract.productization_allowed_now is False
