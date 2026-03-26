from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_flow_map_contract,
)


def test_flow_map_contract_builds() -> None:
    """Flow map contract should build successfully."""
    contract = build_flow_map_contract()

    assert contract.total_steps == 5
    assert len(contract.steps) == 5


def test_flow_map_contains_execution_path() -> None:
    """Flow map should contain control_plane -> execution_control path."""
    contract = build_flow_map_contract()

    pairs = {
        (step.source_component, step.target_component)
        for step in contract.steps
    }

    assert ("control_plane", "execution_control") in pairs
    assert ("execution_control", "workers") in pairs
