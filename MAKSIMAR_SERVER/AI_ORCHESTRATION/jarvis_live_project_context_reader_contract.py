from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_PROJECT_CONTEXT_SOURCES: tuple[str, ...] = (
    "roadmap_status",
    "jarvis_live_ci_status",
    "architecture_summary",
    "test_status_summary",
    "voice_profile_summary",
)


@dataclass(frozen=True, slots=True)
class JarvisLiveProjectContextReaderContract:
    reader_id: str
    read_only: bool = True
    dashboard_safe: bool = True
    project_read_only_summary_allowed: bool = True
    project_context_visible: bool = True
    source_scope: str = "read_only_project_summary"
    allowed_context_sources: tuple[str, ...] = ALLOWED_PROJECT_CONTEXT_SOURCES
    source_file_mutation_allowed: bool = False
    git_operation_allowed: bool = False
    shell_allowed: bool = False
    runtime_mutation_allowed: bool = False
    memory_truth_write_allowed: bool = False
    dashboard_execution_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.reader_id, "reader_id")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_true(
            self.project_read_only_summary_allowed,
            "project_read_only_summary_allowed",
        )
        _require_true(self.project_context_visible, "project_context_visible")
        if self.source_scope != "read_only_project_summary":
            raise ValueError("source_scope must remain read_only_project_summary")
        if self.allowed_context_sources != ALLOWED_PROJECT_CONTEXT_SOURCES:
            raise ValueError("allowed_context_sources must match canonical sources")
        _require_false(self.source_file_mutation_allowed, "source_file_mutation_allowed")
        _require_false(self.git_operation_allowed, "git_operation_allowed")
        _require_false(self.shell_allowed, "shell_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.memory_truth_write_allowed, "memory_truth_write_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "reader_id": self.reader_id,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "project_read_only_summary_allowed": self.project_read_only_summary_allowed,
            "project_context_visible": self.project_context_visible,
            "source_scope": self.source_scope,
            "allowed_context_sources": self.allowed_context_sources,
            "source_file_mutation_allowed": self.source_file_mutation_allowed,
            "git_operation_allowed": self.git_operation_allowed,
            "shell_allowed": self.shell_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "memory_truth_write_allowed": self.memory_truth_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


def build_jarvis_live_project_context_reader_contract() -> (
    JarvisLiveProjectContextReaderContract
):
    return JarvisLiveProjectContextReaderContract(
        reader_id="jarvis_live_project_context_reader_contract_v0_1"
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

