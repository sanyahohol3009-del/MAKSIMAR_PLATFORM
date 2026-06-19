from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.browser_worker_adapter_contract import (
    build_browser_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.cad_cam_worker_adapter_contract import (
    build_cad_cam_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.cli_worker_adapter_contract import (
    build_cli_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import ComputerUseActionRequest
from MAKSIMAR_CORE_LIB.action_library_adapters.gui_worker_adapter_contract import (
    build_gui_worker_adapter_contract,
)
from MAKSIMAR_SERVER.WORKERS.action_recording_runtime import ActionRecording, build_action_recording
from MAKSIMAR_SERVER.WORKERS.action_replay_preview_runtime import (
    ActionReplayPreview,
    build_action_replay_preview,
)


def _contract_by_capability(capability_id: str) -> dict[str, Any]:
    contracts = {
        "browser_worker": build_browser_worker_adapter_contract(),
        "gui_worker": build_gui_worker_adapter_contract(),
        "cli_worker": build_cli_worker_adapter_contract(),
        "cad_cam_worker": build_cad_cam_worker_adapter_contract(),
    }
    if capability_id not in contracts:
        raise ValueError(f"unknown capability_id: {capability_id!r}")
    return contracts[capability_id].to_read_model()


@dataclass(frozen=True, slots=True)
class SandboxedActionWorkerDecision:
    decision_id: str
    request_id: str
    capability_id: str
    action_name: str
    accepted: bool
    direct_execution_allowed: bool
    risk_gate_required: bool
    would_execute: bool
    executed: bool
    denial_reason: str
    recording: ActionRecording
    replay_preview: ActionReplayPreview

    def to_read_model(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "capability_id": self.capability_id,
            "action_name": self.action_name,
            "accepted": self.accepted,
            "direct_execution_allowed": self.direct_execution_allowed,
            "risk_gate_required": self.risk_gate_required,
            "would_execute": self.would_execute,
            "executed": self.executed,
            "denial_reason": self.denial_reason,
            "recording": self.recording.to_read_model(),
            "replay_preview": self.replay_preview.to_read_model(),
        }


def run_sandboxed_action_worker(request: ComputerUseActionRequest) -> SandboxedActionWorkerDecision:
    contract = _contract_by_capability(request.capability_id)
    recording = build_action_recording(request)
    preview = build_action_replay_preview(recording)
    env_execute = os.environ.get("JARVIS_LOCAL_SAFE_ACTION_EXECUTION") == "1"
    verified_owner = request.owner_identity_claim.verified and request.owner_identity_claim.source == "local_terminal_session"
    safe_browser = (
        request.capability_id == "browser_worker"
        and request.action_name == "open_browser"
        and contract["safe_direct_allowed"] is True
        and verified_owner
        and request.input_channel != "voice"
    )
    risk_gate_required = contract["risk_class"] == "risk_gate" or not safe_browser
    executed = bool(safe_browser and env_execute)
    would_execute = bool(safe_browser and not env_execute)
    direct_execution_allowed = bool(safe_browser)
    denial_reason = ""
    if request.input_channel == "voice" and not verified_owner:
        denial_reason = "voice_unverified_cannot_execute_directly"
    elif contract["risk_class"] == "risk_gate":
        denial_reason = "risk_gate_required"
    elif not safe_browser:
        denial_reason = "verified_owner_required_for_safe_direct_action"
    return SandboxedActionWorkerDecision(
        decision_id="sandboxed_action_worker_decision_v1",
        request_id=request.request_id,
        capability_id=request.capability_id,
        action_name=request.action_name,
        accepted=True,
        direct_execution_allowed=direct_execution_allowed,
        risk_gate_required=risk_gate_required,
        would_execute=would_execute,
        executed=executed,
        denial_reason=denial_reason,
        recording=recording,
        replay_preview=preview,
    )
