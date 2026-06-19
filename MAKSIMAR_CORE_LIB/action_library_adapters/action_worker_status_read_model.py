from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime import SandboxedActionWorkerDecision


@dataclass(frozen=True, slots=True)
class ActionWorkerStatusReadModel:
    read_model_id: str
    capability_id: str
    action_name: str
    accepted: bool
    risk_gate_required: bool
    safe_direct_allowed: bool
    would_execute: bool
    executed: bool
    recording_required: bool
    replay_preview_required: bool
    direct_execution_by_swarm: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "capability_id": self.capability_id,
            "action_name": self.action_name,
            "accepted": self.accepted,
            "risk_gate_required": self.risk_gate_required,
            "safe_direct_allowed": self.safe_direct_allowed,
            "would_execute": self.would_execute,
            "executed": self.executed,
            "recording_required": self.recording_required,
            "replay_preview_required": self.replay_preview_required,
            "direct_execution_by_swarm": self.direct_execution_by_swarm,
        }


def build_action_worker_status_read_model(decision: SandboxedActionWorkerDecision) -> ActionWorkerStatusReadModel:
    return ActionWorkerStatusReadModel(
        read_model_id="action_worker_status_read_model_v1",
        capability_id=decision.capability_id,
        action_name=decision.action_name,
        accepted=decision.accepted,
        risk_gate_required=decision.risk_gate_required,
        safe_direct_allowed=decision.direct_execution_allowed,
        would_execute=decision.would_execute,
        executed=decision.executed,
        recording_required=decision.recording.recording_required,
        replay_preview_required=decision.replay_preview.replay_preview_required,
        direct_execution_by_swarm=False,
    )
