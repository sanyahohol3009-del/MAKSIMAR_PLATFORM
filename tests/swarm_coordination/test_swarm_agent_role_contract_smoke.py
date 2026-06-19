from __future__ import annotations

from MAKSIMAR_CORE_LIB.swarm_coordination import (
    SWARM_AGENT_ROLES,
    build_default_swarm_agent_role_contracts,
)


def test_swarm_agent_role_contracts_cover_required_roles() -> None:
    contracts = build_default_swarm_agent_role_contracts()

    assert tuple(contract.role_id for contract in contracts) == SWARM_AGENT_ROLES
    assert all(contract.may_propose for contract in contracts)
    assert all(contract.may_analyze for contract in contracts)
    assert all(contract.may_route for contract in contracts)
    assert all(contract.may_explain for contract in contracts)
    assert all(contract.may_execute_pc_action is False for contract in contracts)
    assert all(contract.may_execute_shell_action is False for contract in contracts)
    assert all(contract.may_write_runtime_state is False for contract in contracts)
    assert all(contract.may_deploy is False for contract in contracts)
    assert all(contract.may_write_canonical_memory is False for contract in contracts)
