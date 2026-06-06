from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_cache_boundary_contract import (
    build_runtime_cache_boundary,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_model_storage_policy_contract import (
    build_runtime_model_storage_policy,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_retrieval_storage_policy_contract import (
    build_runtime_retrieval_storage_policy,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.live_sandbox_vendor_boundary_contract import (
    build_live_sandbox_vendor_boundary_contract,
)


@dataclass(frozen=True, slots=True)
class LiveModelDownloadGateContract:
    gate_id: str
    storage_boundary_ready: bool
    vendor_boundary_ready: bool
    model_download_gate_ready: bool
    controlled_download_allowed: bool
    allowed_runtime_roots: tuple[str, ...]
    allowed_download_candidates: tuple[str, ...]
    blocked_storage_targets: tuple[str, ...]
    actual_download_started: bool = False
    runtime_start_allowed: bool = False
    model_execution_allowed: bool = False
    voice_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.gate_id, "gate_id")
        _require_true(self.storage_boundary_ready, "storage_boundary_ready")
        _require_true(self.vendor_boundary_ready, "vendor_boundary_ready")
        _require_true(self.model_download_gate_ready, "model_download_gate_ready")
        _require_true(self.controlled_download_allowed, "controlled_download_allowed")
        _require_non_empty_tuple(self.allowed_runtime_roots, "allowed_runtime_roots")
        _require_non_empty_tuple(
            self.allowed_download_candidates,
            "allowed_download_candidates",
        )
        _require_non_empty_tuple(self.blocked_storage_targets, "blocked_storage_targets")
        for root in self.allowed_runtime_roots:
            if not root.startswith("~/MAKSIMAR_RUNTIME/runtime_"):
                raise ValueError("download roots must stay under ~/MAKSIMAR_RUNTIME")
        _require_false(self.actual_download_started, "actual_download_started")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_execution_allowed, "model_execution_allowed")
        _require_false(self.voice_allowed, "voice_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "storage_boundary_ready": self.storage_boundary_ready,
            "vendor_boundary_ready": self.vendor_boundary_ready,
            "model_download_gate_ready": self.model_download_gate_ready,
            "controlled_download_allowed": self.controlled_download_allowed,
            "actual_download_started": self.actual_download_started,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_execution_allowed": self.model_execution_allowed,
            "voice_allowed": self.voice_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
            "allowed_runtime_roots": self.allowed_runtime_roots,
            "allowed_download_candidates": self.allowed_download_candidates,
            "blocked_storage_targets": self.blocked_storage_targets,
        }


def build_live_model_download_gate_contract() -> LiveModelDownloadGateContract:
    model_policy = build_runtime_model_storage_policy()
    retrieval_policy = build_runtime_retrieval_storage_policy()
    cache_boundary = build_runtime_cache_boundary()
    vendor_boundary = build_live_sandbox_vendor_boundary_contract()
    vendor_read_model = vendor_boundary.to_read_model()

    return LiveModelDownloadGateContract(
        gate_id="live_model_download_gate_contract_v0_1",
        storage_boundary_ready=(
            model_policy.read_only
            and retrieval_policy.read_only
            and cache_boundary.read_only
            and cache_boundary.dashboard_safe
        ),
        vendor_boundary_ready=vendor_boundary.read_only and vendor_boundary.dashboard_safe,
        model_download_gate_ready=True,
        controlled_download_allowed=True,
        allowed_runtime_roots=vendor_read_model["allowed_runtime_roots"],
        allowed_download_candidates=vendor_read_model["allowed_download_candidate_ids"],
        blocked_storage_targets=vendor_read_model["blocked_storage_targets"],
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    for item in value:
        _require_non_empty(item, field_name)


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

