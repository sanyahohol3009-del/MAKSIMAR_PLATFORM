from __future__ import annotations

from MAKSIMAR_CORE_LIB.swarm_coordination import build_default_swarm_authority_boundary_contract
from MAKSIMAR_SERVER.MEMORY_SYNC.senior_to_junior_model_sync_contract import (
    build_senior_to_junior_model_sync_contract,
)


def test_swarm_respects_existing_mobile_junior_sync_boundary() -> None:
    sync = build_senior_to_junior_model_sync_contract().to_read_model()
    swarm = build_default_swarm_authority_boundary_contract().to_read_model()

    assert sync["mobile_junior_is_subordinate"] is True
    assert sync["junior_core_action_execution_allowed"] is False
    assert sync["junior_shell_execution_allowed"] is False
    assert swarm["swarm_direct_execution_allowed"] is False
    assert swarm["swarm_can_execute_actions"] is False
