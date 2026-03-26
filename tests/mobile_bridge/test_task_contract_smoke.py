from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge import (
    build_task_envelope_contract,
)


def test_task_envelope_contract_builds() -> None:
    """Task envelope contract should build successfully."""
    contract = build_task_envelope_contract()

    assert contract.total_envelopes == 2
    assert len(contract.envelopes) == 2


def test_task_envelope_contract_is_core_safe() -> None:
    """Task envelopes should stay core-safe and mobile-safe."""
    contract = build_task_envelope_contract()

    assert contract.envelopes[0].core_write_allowed is False
    assert contract.envelopes[0].mobile_executes_task is False
    assert contract.envelopes[-1].core_write_allowed is False
    assert contract.envelopes[-1].mobile_executes_task is False
