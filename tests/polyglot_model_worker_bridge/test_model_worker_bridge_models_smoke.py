from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_model_worker_bridge_contract


def test_model_worker_bridge_models_smoke() -> None:
    contract = build_model_worker_bridge_contract()

    assert contract.model_worker_bridge_models_ready is True
    assert contract.missing_required_surfaces == ()
    assert len(contract.bridges) >= 4
    assert contract.productization_allowed_now is False
    assert contract.productization_allowed_next is True
