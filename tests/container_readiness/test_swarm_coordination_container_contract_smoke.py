from __future__ import annotations

from pathlib import Path


CONTRACT_PATH = Path("CONTAINER_DEPLOYMENT/cubes/swarm_coordination/container_contract.yaml")


def test_swarm_coordination_container_contract_smoke() -> None:
    text = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "id: swarm_coordination_container_contract_v1" in text
    assert "cube_id: swarm_coordination" in text
    assert "container_ready: true" in text
    assert "read_model_only: true" in text
    assert "runtime_mutation_allowed: false" in text
    assert "direct_execution_allowed: false" in text
    assert "opens_ports: false" in text
    assert "safe_action_delegated_to: action_library" in text
