from __future__ import annotations

from pathlib import Path


CONTRACT_PATH = Path("CONTAINER_DEPLOYMENT/cubes/action_library/container_contract.yaml")


def test_action_library_container_contract_smoke() -> None:
    text = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "id: action_library_container_contract_v1" in text
    assert "cube_id: action_library" in text
    assert "container_ready: true" in text
    assert "runtime_mutation_allowed: false" in text
    assert "broad_host_mutation_allowed: false" in text
    assert "risk_gate_enabled: true" in text
