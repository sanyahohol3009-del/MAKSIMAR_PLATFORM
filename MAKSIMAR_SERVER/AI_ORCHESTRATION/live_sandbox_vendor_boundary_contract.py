from __future__ import annotations

from dataclasses import dataclass
from typing import Any


APPROVED_VENDOR_CANDIDATE_IDS: tuple[str, ...] = (
    "ollama",
    "kokoro",
    "faster_whisper",
    "vision_ocr",
)

ALLOWED_DOWNLOAD_CANDIDATE_IDS: tuple[str, ...] = (
    "ollama_qwen2_5_coder_14b",
    "kokoro_tts_candidate",
    "faster_whisper_candidate",
    "ocr_vision_candidate",
)

ALLOWED_LIVE_SANDBOX_RUNTIME_ROOTS: tuple[str, ...] = (
    "~/MAKSIMAR_RUNTIME/runtime_models/",
    "~/MAKSIMAR_RUNTIME/runtime_retrieval/",
    "~/MAKSIMAR_RUNTIME/runtime_embeddings/",
    "~/MAKSIMAR_RUNTIME/runtime_vector_indexes/",
    "~/MAKSIMAR_RUNTIME/runtime_rag_cache/",
)

BLOCKED_LIVE_SANDBOX_STORAGE_TARGETS: tuple[str, ...] = (
    "git repo",
    "MAKSIMAR_CORE_LIB",
    "MAKSIMAR_SERVER",
    "memory_engine canonical truth",
    "oob_dashboard",
    "tests",
    "docs",
    ".git",
)


@dataclass(frozen=True, slots=True)
class LiveSandboxVendorBoundaryContract:
    boundary_id: str
    approved_vendor_candidate_ids: tuple[str, ...]
    allowed_download_candidate_ids: tuple[str, ...]
    allowed_runtime_roots: tuple[str, ...]
    blocked_storage_targets: tuple[str, ...]
    git_storage_allowed: bool = False
    core_storage_allowed: bool = False
    server_canonical_storage_allowed: bool = False
    dashboard_storage_allowed: bool = False
    memory_truth_write_allowed: bool = False
    tests_storage_allowed: bool = False
    docs_storage_allowed: bool = False
    external_network_call_allowed: bool = False
    actual_download_started: bool = False
    runtime_start_allowed: bool = False
    model_execution_allowed: bool = False
    dashboard_execution_allowed: bool = False
    read_only: bool = True
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.boundary_id, "boundary_id")
        _require_exact_tuple(
            self.approved_vendor_candidate_ids,
            APPROVED_VENDOR_CANDIDATE_IDS,
            "approved_vendor_candidate_ids",
        )
        _require_exact_tuple(
            self.allowed_download_candidate_ids,
            ALLOWED_DOWNLOAD_CANDIDATE_IDS,
            "allowed_download_candidate_ids",
        )
        _require_exact_tuple(
            self.allowed_runtime_roots,
            ALLOWED_LIVE_SANDBOX_RUNTIME_ROOTS,
            "allowed_runtime_roots",
        )
        _require_exact_tuple(
            self.blocked_storage_targets,
            BLOCKED_LIVE_SANDBOX_STORAGE_TARGETS,
            "blocked_storage_targets",
        )
        for root in self.allowed_runtime_roots:
            if not root.startswith("~/MAKSIMAR_RUNTIME/runtime_"):
                raise ValueError("allowed runtime roots must live under ~/MAKSIMAR_RUNTIME")
        _require_false(self.git_storage_allowed, "git_storage_allowed")
        _require_false(self.core_storage_allowed, "core_storage_allowed")
        _require_false(
            self.server_canonical_storage_allowed,
            "server_canonical_storage_allowed",
        )
        _require_false(self.dashboard_storage_allowed, "dashboard_storage_allowed")
        _require_false(self.memory_truth_write_allowed, "memory_truth_write_allowed")
        _require_false(self.tests_storage_allowed, "tests_storage_allowed")
        _require_false(self.docs_storage_allowed, "docs_storage_allowed")
        _require_false(self.external_network_call_allowed, "external_network_call_allowed")
        _require_false(self.actual_download_started, "actual_download_started")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_execution_allowed, "model_execution_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "approved_vendor_candidate_ids": self.approved_vendor_candidate_ids,
            "allowed_download_candidate_ids": self.allowed_download_candidate_ids,
            "allowed_runtime_roots": self.allowed_runtime_roots,
            "blocked_storage_targets": self.blocked_storage_targets,
            "git_storage_allowed": self.git_storage_allowed,
            "core_storage_allowed": self.core_storage_allowed,
            "server_canonical_storage_allowed": self.server_canonical_storage_allowed,
            "dashboard_storage_allowed": self.dashboard_storage_allowed,
            "memory_truth_write_allowed": self.memory_truth_write_allowed,
            "tests_storage_allowed": self.tests_storage_allowed,
            "docs_storage_allowed": self.docs_storage_allowed,
            "external_network_call_allowed": self.external_network_call_allowed,
            "actual_download_started": self.actual_download_started,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_execution_allowed": self.model_execution_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
        }


def build_live_sandbox_vendor_boundary_contract() -> LiveSandboxVendorBoundaryContract:
    return LiveSandboxVendorBoundaryContract(
        boundary_id="live_sandbox_vendor_boundary_contract_v0_1",
        approved_vendor_candidate_ids=APPROVED_VENDOR_CANDIDATE_IDS,
        allowed_download_candidate_ids=ALLOWED_DOWNLOAD_CANDIDATE_IDS,
        allowed_runtime_roots=ALLOWED_LIVE_SANDBOX_RUNTIME_ROOTS,
        blocked_storage_targets=BLOCKED_LIVE_SANDBOX_STORAGE_TARGETS,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_exact_tuple(
    value: tuple[str, ...],
    expected: tuple[str, ...],
    field_name: str,
) -> None:
    if value != expected:
        raise ValueError(f"{field_name} must match canonical values")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

