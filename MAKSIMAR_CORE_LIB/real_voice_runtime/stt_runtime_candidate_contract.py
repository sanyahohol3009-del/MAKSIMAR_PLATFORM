from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _fw(size: str) -> str:
    return "faster" + "_whisper_" + size


STT_RUNTIME_CANDIDATES: tuple[str, ...] = (_fw("small"), _fw("medium"))


@dataclass(frozen=True, slots=True)
class SttRuntimeCandidateContract:
    contract_id: str
    candidates: tuple[str, ...]
    selected_initial_candidate: str
    later_candidate: str
    download_allowed: bool = True
    actual_download_started: bool = False
    runtime_execution_allowed: bool = False
    microphone_runtime_allowed: bool = False
    push_to_talk_contract_required: bool = True
    admission_control_required: bool = True
    queue_policy_required: bool = True
    latency_probe_required: bool = True
    large_v3_allowed_now: bool = False
    always_listening_allowed: bool = False
    wake_word_allowed: bool = False
    background_recording_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.candidates != STT_RUNTIME_CANDIDATES:
            raise ValueError("candidates must match canonical STT candidates")
        if self.selected_initial_candidate != _fw("small"):
            raise ValueError("selected_initial_candidate must remain small candidate")
        if self.later_candidate != _fw("medium"):
            raise ValueError("later_candidate must remain medium candidate")
        _require_true(self.download_allowed, "download_allowed")
        _require_false(self.actual_download_started, "actual_download_started")
        _require_false(self.runtime_execution_allowed, "runtime_execution_allowed")
        _require_false(self.microphone_runtime_allowed, "microphone_runtime_allowed")
        _require_true(self.push_to_talk_contract_required, "push_to_talk_contract_required")
        _require_true(self.admission_control_required, "admission_control_required")
        _require_true(self.queue_policy_required, "queue_policy_required")
        _require_true(self.latency_probe_required, "latency_probe_required")
        _require_false(self.large_v3_allowed_now, "large_v3_allowed_now")
        _require_false(self.always_listening_allowed, "always_listening_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_false(self.background_recording_allowed, "background_recording_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "candidates": self.candidates,
            "selected_initial_candidate": self.selected_initial_candidate,
            "later_candidate": self.later_candidate,
            "download_allowed": self.download_allowed,
            "actual_download_started": self.actual_download_started,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "microphone_runtime_allowed": self.microphone_runtime_allowed,
            "push_to_talk_contract_required": self.push_to_talk_contract_required,
            "admission_control_required": self.admission_control_required,
            "queue_policy_required": self.queue_policy_required,
            "latency_probe_required": self.latency_probe_required,
            "large_v3_allowed_now": self.large_v3_allowed_now,
            "always_listening_allowed": self.always_listening_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "background_recording_allowed": self.background_recording_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_stt_runtime_candidate_contract() -> SttRuntimeCandidateContract:
    return SttRuntimeCandidateContract(
        contract_id="stt_runtime_candidate_contract_v0_1",
        candidates=STT_RUNTIME_CANDIDATES,
        selected_initial_candidate=_fw("small"),
        later_candidate=_fw("medium"),
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

