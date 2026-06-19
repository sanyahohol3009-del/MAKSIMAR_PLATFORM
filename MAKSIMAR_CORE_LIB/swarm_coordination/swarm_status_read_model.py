from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SwarmStatusReadModel:
    read_model_id: str
    active_agents: tuple[str, ...]
    selected_model_role: str
    selected_tools: tuple[str, ...]
    conflict_status: str
    heavy_gpu_lock_status: str
    direct_execution_disabled_for_swarm: bool
    safe_action_delegated_to_action_library: bool

    def __post_init__(self) -> None:
        if not isinstance(self.read_model_id, str) or not self.read_model_id.strip():
            raise ValueError("read_model_id must be a non-empty string")
        if not self.active_agents:
            raise ValueError("active_agents must not be empty")
        if not isinstance(self.selected_model_role, str) or not self.selected_model_role.strip():
            raise ValueError("selected_model_role must be a non-empty string")
        if not isinstance(self.conflict_status, str) or not self.conflict_status.strip():
            raise ValueError("conflict_status must be a non-empty string")
        if not isinstance(self.heavy_gpu_lock_status, str) or not self.heavy_gpu_lock_status.strip():
            raise ValueError("heavy_gpu_lock_status must be a non-empty string")
        if self.direct_execution_disabled_for_swarm is not True:
            raise ValueError("direct_execution_disabled_for_swarm must be True")
        if self.safe_action_delegated_to_action_library is not True:
            raise ValueError("safe_action_delegated_to_action_library must be True")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "active_agents": self.active_agents,
            "selected_model_role": self.selected_model_role,
            "selected_tools": self.selected_tools,
            "conflict_status": self.conflict_status,
            "heavy_gpu_lock_status": self.heavy_gpu_lock_status,
            "direct_execution_disabled_for_swarm": self.direct_execution_disabled_for_swarm,
            "safe_action_delegated_to_action_library": self.safe_action_delegated_to_action_library,
        }
