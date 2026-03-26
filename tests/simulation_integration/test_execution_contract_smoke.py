from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration import (
    SimulationIntent,
    build_simulation_execution_contract,
    build_simulation_execution_envelope,
)


def test_execution_contract_builds() -> None:
    """Execution contract should be created correctly."""
    envelope = build_simulation_execution_envelope(
        SimulationIntent(query_text="simulate robot arm")
    )
    contract = build_simulation_execution_contract(envelope)

    assert contract.execution_id == envelope.execution_id
    assert contract.backend_id == envelope.backend_id
    assert contract.sandbox_required is True
    assert contract.network_access is False
    assert contract.write_to_core_allowed is False
    assert contract.status == "ready_for_sandbox"


def test_execution_contract_payload_ref_is_stable() -> None:
    """Execution contract should contain stable payload reference."""
    envelope = build_simulation_execution_envelope(
        SimulationIntent(
            query_text="simulate cartpole",
            preferred_backend="simulation_backend_pybullet",
        )
    )
    contract = build_simulation_execution_contract(envelope)

    assert contract.payload_ref.startswith(envelope.execution_id)
    assert envelope.source_definition_id in contract.payload_ref
