from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SwarmAgentHealthReadModel:
    read_model_id: str
    agent_role: str
    status: str
    selected_model_role: str
    heavy_gpu_candidate: bool
    direct_execution_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("read_model_id", "agent_role", "status", "selected_model_role"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.direct_execution_allowed is not False:
            raise ValueError("direct_execution_allowed must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "agent_role": self.agent_role,
            "status": self.status,
            "selected_model_role": self.selected_model_role,
            "heavy_gpu_candidate": self.heavy_gpu_candidate,
            "direct_execution_allowed": self.direct_execution_allowed,
        }
