from __future__ import annotations

from MAKSIMAR_CORE_LIB.swarm_coordination import build_default_swarm_authority_boundary_contract


def test_swarm_authority_boundary_contract_enforces_required_flags() -> None:
    read_model = build_default_swarm_authority_boundary_contract().to_read_model()

    assert read_model["swarm_direct_execution_allowed"] is False
    assert read_model["swarm_can_select_tools"] is True
    assert read_model["swarm_can_select_models"] is True
    assert read_model["swarm_can_propose_actions"] is True
    assert read_model["swarm_can_execute_actions"] is False
    assert read_model["verified_owner_safe_action_required"] is True
