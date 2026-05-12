from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_review_contract


def test_sandbox_review_models_smoke() -> None:
    contract = build_sandbox_review_contract()

    assert contract.sandbox_review_ready is True
    assert contract.phase_id == "PHASE 6.4"
    assert contract.sandbox_binding_ready is True
    assert contract.sandbox_result_reader_ready is True
    assert contract.simulation_result_reader_ready is True
    assert contract.evaluation_result_reader_ready is True
    assert contract.owner_review_package_ready is True
    assert contract.direct_core_write_allowed is False
    assert contract.auto_apply_allowed is False
