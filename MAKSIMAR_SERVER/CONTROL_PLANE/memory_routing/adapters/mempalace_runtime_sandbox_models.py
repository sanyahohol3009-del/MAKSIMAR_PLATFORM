from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_preview_builder import (
    build_mempalace_preview,
)

_VENDOR_GATE_REPORT = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json")


def _load_vendor_gate_report() -> dict[str, object]:
    if not _VENDOR_GATE_REPORT.exists():
        raise FileNotFoundError(f"vendor gate report missing: {_VENDOR_GATE_REPORT}")

    return json.loads(_VENDOR_GATE_REPORT.read_text(encoding="utf-8"))


@dataclass(frozen=True, slots=True)
class MemPalaceRuntimeSandboxPolicy:
    policy_id: str
    adapter_id: str
    hard_gate_passed: bool
    manual_security_review_required: bool
    fake_backend_required: bool
    fake_backend_allowed: bool
    real_backend_candidate_allowed: bool
    real_backend_enablement_allowed: bool
    query_only_allowed: bool
    read_only_allowed: bool
    evidence_pack_required: bool
    preview_trace_required: bool
    canonical_write_allowed: bool
    auto_promotion_allowed: bool
    auto_conflict_resolution_allowed: bool
    runtime_mutation_allowed: bool
    sandbox_policy_ready: bool
    evidence_sources: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if not self.adapter_id:
            raise ValueError("adapter_id must be non-empty")
        if not isinstance(self.evidence_sources, tuple) or not self.evidence_sources:
            raise ValueError("evidence_sources must be a non-empty tuple")

        required_true_fields = (
            "hard_gate_passed",
            "manual_security_review_required",
            "fake_backend_required",
            "fake_backend_allowed",
            "real_backend_candidate_allowed",
            "query_only_allowed",
            "read_only_allowed",
            "evidence_pack_required",
            "preview_trace_required",
            "sandbox_policy_ready",
        )

        for field_name in required_true_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")
            if not value:
                raise ValueError(f"{field_name} must be True")

        required_false_fields = (
            "real_backend_enablement_allowed",
            "canonical_write_allowed",
            "auto_promotion_allowed",
            "auto_conflict_resolution_allowed",
            "runtime_mutation_allowed",
        )

        for field_name in required_false_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")
            if value:
                raise ValueError(f"{field_name} must be False")


def build_mempalace_runtime_sandbox_policy() -> MemPalaceRuntimeSandboxPolicy:
    preview = build_mempalace_preview()
    gate_report = _load_vendor_gate_report()

    hard_gate_passed = bool(gate_report["hard_gate_passed"])
    manual_review_required = bool(gate_report["manual_security_review_required"])

    sandbox_policy_ready = (
        bool(preview["preview_ready"])
        and hard_gate_passed
        and manual_review_required
        and preview["external_backend_connected"] is False
        and preview["real_backend_enabled"] is False
        and preview["canonical_write_allowed"] == 0
        and preview["runtime_mutation_allowed"] == 0
    )

    return MemPalaceRuntimeSandboxPolicy(
        policy_id="mempalace_runtime_sandbox_policy_001",
        adapter_id="mempalace_adapter_memory_routing_001",
        hard_gate_passed=hard_gate_passed,
        manual_security_review_required=manual_review_required,
        fake_backend_required=True,
        fake_backend_allowed=True,
        real_backend_candidate_allowed=hard_gate_passed,
        real_backend_enablement_allowed=False,
        query_only_allowed=True,
        read_only_allowed=True,
        evidence_pack_required=True,
        preview_trace_required=True,
        canonical_write_allowed=False,
        auto_promotion_allowed=False,
        auto_conflict_resolution_allowed=False,
        runtime_mutation_allowed=False,
        sandbox_policy_ready=sandbox_policy_ready,
        evidence_sources=(
            "EXTERNAL_BACKENDS/mempalace/manifests/mempalace_source_manifest.json",
            "EXTERNAL_BACKENDS/mempalace/manifests/mempalace_version_lock.json",
            "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_sandbox_smoke_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json",
        ),
    )
