from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.swarm_coordination.swarm_agent_role_contract import SWARM_AGENT_ROLES


@dataclass(frozen=True, slots=True)
class SwarmTaskContract:
    task_id: str
    user_text: str
    input_channel: str
    normalized_intent: str
    selected_model_role_id: str
    selected_model_id: str
    selected_tools: tuple[str, ...]
    candidate_agent_roles: tuple[str, ...]
    task_complexity: str
    heavy_model_requested: bool
    risk_gate_required: bool
    safe_direct_action_candidate: bool
    read_only_discovery_only: bool
    owner_identity_source: str
    direct_execution_requested: bool

    def __post_init__(self) -> None:
        for field_name in (
            "task_id",
            "user_text",
            "input_channel",
            "normalized_intent",
            "selected_model_role_id",
            "selected_model_id",
            "task_complexity",
            "owner_identity_source",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.input_channel not in {"text", "voice", "screen"}:
            raise ValueError(f"unsupported input_channel: {self.input_channel!r}")
        if not self.candidate_agent_roles:
            raise ValueError("candidate_agent_roles must not be empty")
        unknown_roles = set(self.candidate_agent_roles) - set(SWARM_AGENT_ROLES)
        if unknown_roles:
            raise ValueError(f"unknown candidate_agent_roles: {sorted(unknown_roles)!r}")
        if self.task_complexity not in {"light", "medium", "heavy"}:
            raise ValueError(f"unsupported task_complexity: {self.task_complexity!r}")
        if self.safe_direct_action_candidate and self.risk_gate_required:
            raise ValueError("safe_direct_action_candidate cannot be true when risk_gate_required is true")
        if self.read_only_discovery_only and self.direct_execution_requested:
            raise ValueError("read_only_discovery_only cannot request direct execution")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "user_text": self.user_text,
            "input_channel": self.input_channel,
            "normalized_intent": self.normalized_intent,
            "selected_model_role_id": self.selected_model_role_id,
            "selected_model_id": self.selected_model_id,
            "selected_tools": self.selected_tools,
            "candidate_agent_roles": self.candidate_agent_roles,
            "task_complexity": self.task_complexity,
            "heavy_model_requested": self.heavy_model_requested,
            "risk_gate_required": self.risk_gate_required,
            "safe_direct_action_candidate": self.safe_direct_action_candidate,
            "read_only_discovery_only": self.read_only_discovery_only,
            "owner_identity_source": self.owner_identity_source,
            "direct_execution_requested": self.direct_execution_requested,
        }
