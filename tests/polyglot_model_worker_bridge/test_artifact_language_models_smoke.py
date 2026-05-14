from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_artifact_language_contract


def test_artifact_language_models_smoke() -> None:
    contract = build_artifact_language_contract()

    assert contract.artifact_language_models_ready is True
    assert len(contract.entries) >= 5
    assert contract.source_bound_required is True
    assert contract.artifact_ref_required is True
    assert contract.build_test_route_required is True
    assert contract.productization_allowed_now is False
