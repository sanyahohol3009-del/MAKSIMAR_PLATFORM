from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisLiveTextLoopAdapterContract:
    adapter_id: str
    read_only: bool = True
    dashboard_safe: bool = True
    text_input_allowed: bool = True
    llm_answer_allowed: bool = True
    qwen_model_available: bool = True
    qwen_probe_passed: bool = True
    model_id: str = "qwen2.5-coder:14b"
    model_runtime_root: str = "/home/aleksandr/MAKSIMAR_RUNTIME/runtime_models/ollama"
    project_context_reader_required: bool = True
    tts_output_allowed: bool = True
    shell_allowed: bool = False
    file_edit_allowed: bool = False
    git_allowed: bool = False
    app_control_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False
    autonomous_loop_allowed: bool = False
    microphone_allowed: bool = False
    stt_allowed: bool = False
    wake_word_allowed: bool = False
    owner_command_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_id, "adapter_id")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_true(self.text_input_allowed, "text_input_allowed")
        _require_true(self.llm_answer_allowed, "llm_answer_allowed")
        _require_true(self.qwen_model_available, "qwen_model_available")
        _require_true(self.qwen_probe_passed, "qwen_probe_passed")
        if self.model_id != "qwen2.5-coder:14b":
            raise ValueError("model_id must remain qwen2.5-coder:14b")
        if self.model_runtime_root != "/home/aleksandr/MAKSIMAR_RUNTIME/runtime_models/ollama":
            raise ValueError("model_runtime_root must remain outside the git repository")
        _require_true(self.project_context_reader_required, "project_context_reader_required")
        _require_true(self.tts_output_allowed, "tts_output_allowed")
        _require_false(self.shell_allowed, "shell_allowed")
        _require_false(self.file_edit_allowed, "file_edit_allowed")
        _require_false(self.git_allowed, "git_allowed")
        _require_false(self.app_control_allowed, "app_control_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.autonomous_loop_allowed, "autonomous_loop_allowed")
        _require_false(self.microphone_allowed, "microphone_allowed")
        _require_false(self.stt_allowed, "stt_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "text_input_allowed": self.text_input_allowed,
            "llm_answer_allowed": self.llm_answer_allowed,
            "qwen_model_available": self.qwen_model_available,
            "qwen_probe_passed": self.qwen_probe_passed,
            "model_id": self.model_id,
            "model_runtime_root": self.model_runtime_root,
            "project_context_reader_required": self.project_context_reader_required,
            "tts_output_allowed": self.tts_output_allowed,
            "shell_allowed": self.shell_allowed,
            "file_edit_allowed": self.file_edit_allowed,
            "git_allowed": self.git_allowed,
            "app_control_allowed": self.app_control_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "autonomous_loop_allowed": self.autonomous_loop_allowed,
            "microphone_allowed": self.microphone_allowed,
            "stt_allowed": self.stt_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "owner_command_required": self.owner_command_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
        }


def build_jarvis_live_text_loop_adapter_contract() -> JarvisLiveTextLoopAdapterContract:
    return JarvisLiveTextLoopAdapterContract(
        adapter_id="jarvis_live_text_loop_adapter_contract_v0_1"
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

