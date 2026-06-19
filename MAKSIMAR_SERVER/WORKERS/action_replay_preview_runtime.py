from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.WORKERS.action_recording_runtime import ActionRecording


@dataclass(frozen=True, slots=True)
class ActionReplayPreview:
    preview_id: str
    request_id: str
    replay_preview_required: bool
    preview_steps: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "preview_id": self.preview_id,
            "request_id": self.request_id,
            "replay_preview_required": self.replay_preview_required,
            "preview_steps": self.preview_steps,
        }


def build_action_replay_preview(recording: ActionRecording) -> ActionReplayPreview:
    preview_steps = recording.recorded_steps + ("await_operator_or_env_execution",)
    return ActionReplayPreview(
        preview_id="action_replay_preview_v1",
        request_id=recording.request_id,
        replay_preview_required=True,
        preview_steps=preview_steps,
    )
