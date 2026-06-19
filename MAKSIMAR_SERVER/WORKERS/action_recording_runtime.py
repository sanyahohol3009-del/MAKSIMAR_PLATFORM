from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import ComputerUseActionRequest


@dataclass(frozen=True, slots=True)
class ActionRecording:
    record_id: str
    request_id: str
    capability_id: str
    action_name: str
    recording_required: bool
    recorded_steps: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "capability_id": self.capability_id,
            "action_name": self.action_name,
            "recording_required": self.recording_required,
            "recorded_steps": self.recorded_steps,
        }


def build_action_recording(request: ComputerUseActionRequest) -> ActionRecording:
    steps = (
        "validate_owner_identity",
        f"check_capability:{request.capability_id}",
        f"check_risk_class:{request.risk_class}",
        f"prepare_action:{request.action_name}",
        f"target:{request.target}",
    )
    return ActionRecording(
        record_id="action_recording_v1",
        request_id=request.request_id,
        capability_id=request.capability_id,
        action_name=request.action_name,
        recording_required=True,
        recorded_steps=steps,
    )
