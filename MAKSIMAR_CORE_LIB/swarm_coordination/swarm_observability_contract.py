from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SwarmObservabilityContract:
    contract_id: str
    tracks_active_agents: bool
    tracks_selected_model_role: bool
    tracks_selected_tools: bool
    tracks_conflict_status: bool
    tracks_heavy_gpu_lock_status: bool
    direct_execution_disabled_for_swarm: bool
    safe_action_delegated_to_action_library: bool
    read_only: bool
    dashboard_safe: bool

    def __post_init__(self) -> None:
        if not isinstance(self.contract_id, str) or not self.contract_id.strip():
            raise ValueError("contract_id must be a non-empty string")
        for field_name in (
            "tracks_active_agents",
            "tracks_selected_model_role",
            "tracks_selected_tools",
            "tracks_conflict_status",
            "tracks_heavy_gpu_lock_status",
            "direct_execution_disabled_for_swarm",
            "safe_action_delegated_to_action_library",
            "read_only",
            "dashboard_safe",
        ):
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "tracks_active_agents": self.tracks_active_agents,
            "tracks_selected_model_role": self.tracks_selected_model_role,
            "tracks_selected_tools": self.tracks_selected_tools,
            "tracks_conflict_status": self.tracks_conflict_status,
            "tracks_heavy_gpu_lock_status": self.tracks_heavy_gpu_lock_status,
            "direct_execution_disabled_for_swarm": self.direct_execution_disabled_for_swarm,
            "safe_action_delegated_to_action_library": self.safe_action_delegated_to_action_library,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
        }


def build_default_swarm_observability_contract() -> SwarmObservabilityContract:
    return SwarmObservabilityContract(
        contract_id="swarm_observability_contract_v1",
        tracks_active_agents=True,
        tracks_selected_model_role=True,
        tracks_selected_tools=True,
        tracks_conflict_status=True,
        tracks_heavy_gpu_lock_status=True,
        direct_execution_disabled_for_swarm=True,
        safe_action_delegated_to_action_library=True,
        read_only=True,
        dashboard_safe=True,
    )
