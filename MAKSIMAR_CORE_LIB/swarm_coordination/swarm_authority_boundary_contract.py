from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SwarmAuthorityBoundaryContract:
    boundary_id: str
    swarm_direct_execution_allowed: bool
    swarm_can_select_tools: bool
    swarm_can_select_models: bool
    swarm_can_propose_actions: bool
    swarm_can_execute_actions: bool
    verified_owner_safe_action_required: bool

    def __post_init__(self) -> None:
        if not isinstance(self.boundary_id, str) or not self.boundary_id.strip():
            raise ValueError("boundary_id must be a non-empty string")
        if self.swarm_direct_execution_allowed is not False:
            raise ValueError("swarm_direct_execution_allowed must be False")
        if self.swarm_can_select_tools is not True:
            raise ValueError("swarm_can_select_tools must be True")
        if self.swarm_can_select_models is not True:
            raise ValueError("swarm_can_select_models must be True")
        if self.swarm_can_propose_actions is not True:
            raise ValueError("swarm_can_propose_actions must be True")
        if self.swarm_can_execute_actions is not False:
            raise ValueError("swarm_can_execute_actions must be False")
        if self.verified_owner_safe_action_required is not True:
            raise ValueError("verified_owner_safe_action_required must be True")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "swarm_direct_execution_allowed": self.swarm_direct_execution_allowed,
            "swarm_can_select_tools": self.swarm_can_select_tools,
            "swarm_can_select_models": self.swarm_can_select_models,
            "swarm_can_propose_actions": self.swarm_can_propose_actions,
            "swarm_can_execute_actions": self.swarm_can_execute_actions,
            "verified_owner_safe_action_required": self.verified_owner_safe_action_required,
        }


def build_default_swarm_authority_boundary_contract() -> SwarmAuthorityBoundaryContract:
    return SwarmAuthorityBoundaryContract(
        boundary_id="swarm_authority_boundary_contract_v1",
        swarm_direct_execution_allowed=False,
        swarm_can_select_tools=True,
        swarm_can_select_models=True,
        swarm_can_propose_actions=True,
        swarm_can_execute_actions=False,
        verified_owner_safe_action_required=True,
    )
