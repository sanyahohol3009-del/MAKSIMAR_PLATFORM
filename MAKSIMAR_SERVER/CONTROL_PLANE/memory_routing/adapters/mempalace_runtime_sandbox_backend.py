from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_models import (
    build_mempalace_runtime_sandbox_policy,
)

_SMOKE_REPORT = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_sandbox_smoke_report.json")
_VENDOR_GATE_REPORT = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json")


@dataclass(frozen=True, slots=True)
class MemPalaceSandboxQueryResult:
    query_id: str
    backend_kind: str
    query_text: str
    query_only: bool
    read_only: bool
    fake_backend_used: bool
    real_backend_enabled: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    evidence_pack: Tuple[str, ...]
    preview_trace: Tuple[str, ...]
    result_ready: bool

    def __post_init__(self) -> None:
        if not self.query_id:
            raise ValueError("query_id must be non-empty")
        if not self.backend_kind:
            raise ValueError("backend_kind must be non-empty")
        if not self.query_text:
            raise ValueError("query_text must be non-empty")
        if not self.evidence_pack:
            raise ValueError("evidence_pack must be non-empty")
        if not self.preview_trace:
            raise ValueError("preview_trace must be non-empty")

        if not self.query_only:
            raise ValueError("query_only must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.fake_backend_used:
            raise ValueError("fake_backend_used must be True")
        if self.real_backend_enabled:
            raise ValueError("real_backend_enabled must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.result_ready:
            raise ValueError("result_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceRealBackendCandidateState:
    candidate_id: str
    vendor_import_smoke_passed: bool
    vendor_gate_hard_passed: bool
    manual_security_review_required: bool
    real_backend_candidate_detected: bool
    real_backend_enabled: bool
    real_backend_query_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    candidate_state_ready: bool

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if not self.vendor_import_smoke_passed:
            raise ValueError("vendor_import_smoke_passed must be True")
        if not self.vendor_gate_hard_passed:
            raise ValueError("vendor_gate_hard_passed must be True")
        if not self.manual_security_review_required:
            raise ValueError("manual_security_review_required must be True")
        if not self.real_backend_candidate_detected:
            raise ValueError("real_backend_candidate_detected must be True")
        if self.real_backend_enabled:
            raise ValueError("real_backend_enabled must be False")
        if self.real_backend_query_allowed:
            raise ValueError("real_backend_query_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.candidate_state_ready:
            raise ValueError("candidate_state_ready must be True")


class FakeMemPalaceSandboxBackend:
    def query(self, query_text: str) -> MemPalaceSandboxQueryResult:
        policy = build_mempalace_runtime_sandbox_policy()

        return MemPalaceSandboxQueryResult(
            query_id="mempalace_fake_sandbox_query_001",
            backend_kind="fake_mempalace_sandbox_backend",
            query_text=query_text,
            query_only=policy.query_only_allowed,
            read_only=policy.read_only_allowed,
            fake_backend_used=True,
            real_backend_enabled=False,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            evidence_pack=policy.evidence_sources,
            preview_trace=(
                "adapter_contract_checked",
                "vendor_gate_report_checked",
                "manual_review_required_detected",
                "fake_backend_query_executed",
                "real_backend_kept_disabled",
            ),
            result_ready=policy.sandbox_policy_ready,
        )


def build_mempalace_fake_backend_query_result() -> MemPalaceSandboxQueryResult:
    backend = FakeMemPalaceSandboxBackend()
    return backend.query("sandbox query for MemPalace adapter readiness")


def build_mempalace_real_backend_candidate_state() -> MemPalaceRealBackendCandidateState:
    if not _SMOKE_REPORT.exists():
        raise FileNotFoundError(f"smoke report missing: {_SMOKE_REPORT}")
    if not _VENDOR_GATE_REPORT.exists():
        raise FileNotFoundError(f"vendor gate report missing: {_VENDOR_GATE_REPORT}")

    smoke = json.loads(_SMOKE_REPORT.read_text(encoding="utf-8"))
    gate = json.loads(_VENDOR_GATE_REPORT.read_text(encoding="utf-8"))

    vendor_import_smoke_passed = bool(smoke["cli_import_smoke_passed"])
    vendor_gate_hard_passed = bool(gate["hard_gate_passed"])
    manual_review_required = bool(gate["manual_security_review_required"])

    return MemPalaceRealBackendCandidateState(
        candidate_id="mempalace_real_backend_candidate_001",
        vendor_import_smoke_passed=vendor_import_smoke_passed,
        vendor_gate_hard_passed=vendor_gate_hard_passed,
        manual_security_review_required=manual_review_required,
        real_backend_candidate_detected=vendor_import_smoke_passed and vendor_gate_hard_passed,
        real_backend_enabled=False,
        real_backend_query_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        candidate_state_ready=vendor_import_smoke_passed and vendor_gate_hard_passed and manual_review_required,
    )
