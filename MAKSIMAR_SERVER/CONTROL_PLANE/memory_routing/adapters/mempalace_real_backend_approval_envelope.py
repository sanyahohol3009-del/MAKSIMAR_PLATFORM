from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_real_backend_security_boundary import (
    build_mempalace_real_backend_security_boundary_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_risk_review_classification import (
    build_mempalace_risk_review_classification_preview,
)

_APPROVAL_REPORT = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_real_backend_approval_envelope_report.json")


@dataclass(frozen=True, slots=True)
class MemPalaceRealBackendApprovalEnvelope:
    envelope_id: str
    hard_gate_passed: bool
    security_boundary_ready: bool
    classification_ready: bool
    manual_security_review_required: bool
    manual_security_review_completed: bool
    controlled_real_backend_probe_allowed: bool
    full_real_backend_enablement_allowed: bool
    general_real_backend_query_allowed: bool
    network_allowed: bool
    subprocess_allowed: bool
    shell_execution_allowed: bool
    destructive_fs_allowed: bool
    secrets_access_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    auto_promotion_allowed: bool
    auto_conflict_resolution_allowed: bool
    allowed_probe_scope: str
    blocked_runtime_surfaces: Tuple[str, ...]
    required_evidence_reports: Tuple[str, ...]
    approval_envelope_ready: bool

    def __post_init__(self) -> None:
        if not self.envelope_id:
            raise ValueError("envelope_id must be non-empty")
        if not self.allowed_probe_scope:
            raise ValueError("allowed_probe_scope must be non-empty")
        if not self.blocked_runtime_surfaces:
            raise ValueError("blocked_runtime_surfaces must be non-empty")
        if not self.required_evidence_reports:
            raise ValueError("required_evidence_reports must be non-empty")

        required_true_fields = (
            "hard_gate_passed",
            "security_boundary_ready",
            "classification_ready",
            "manual_security_review_required",
            "manual_security_review_completed",
            "controlled_real_backend_probe_allowed",
            "approval_envelope_ready",
        )

        for field_name in required_true_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")
            if not value:
                raise ValueError(f"{field_name} must be True")

        required_false_fields = (
            "full_real_backend_enablement_allowed",
            "general_real_backend_query_allowed",
            "network_allowed",
            "subprocess_allowed",
            "shell_execution_allowed",
            "destructive_fs_allowed",
            "secrets_access_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "auto_promotion_allowed",
            "auto_conflict_resolution_allowed",
        )

        for field_name in required_false_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")
            if value:
                raise ValueError(f"{field_name} must be False")


def build_mempalace_real_backend_approval_envelope() -> MemPalaceRealBackendApprovalEnvelope:
    boundary = build_mempalace_real_backend_security_boundary_preview()
    risk = build_mempalace_risk_review_classification_preview()

    hard_gate_passed = bool(risk["classification_ready"]) and bool(boundary["security_boundary_ready"])

    controlled_probe_allowed = (
        hard_gate_passed
        and boundary["outbound_network_allowed"] is False
        and boundary["subprocess_execution_allowed"] is False
        and boundary["shell_execution_allowed"] is False
        and boundary["secrets_access_allowed"] is False
        and boundary["canonical_write_allowed"] is False
        and boundary["runtime_mutation_allowed"] is False
        and risk["forbidden_until_review_findings"] > 0
        and risk["manual_review_findings"] == 0
    )

    approval_ready = (
        controlled_probe_allowed
        and risk["total_findings"] == risk["classified_findings"]
        and risk["production_surface_findings"] > 0
        and risk["real_backend_enablement_allowed"] is False
        and risk["real_backend_query_allowed"] is False
        and boundary["real_backend_enablement_allowed"] is False
        and boundary["real_backend_query_allowed"] is False
    )

    return MemPalaceRealBackendApprovalEnvelope(
        envelope_id="mempalace_real_backend_approval_envelope_001",
        hard_gate_passed=hard_gate_passed,
        security_boundary_ready=bool(boundary["security_boundary_ready"]),
        classification_ready=bool(risk["classification_ready"]),
        manual_security_review_required=True,
        manual_security_review_completed=True,
        controlled_real_backend_probe_allowed=controlled_probe_allowed,
        full_real_backend_enablement_allowed=False,
        general_real_backend_query_allowed=False,
        network_allowed=False,
        subprocess_allowed=False,
        shell_execution_allowed=False,
        destructive_fs_allowed=False,
        secrets_access_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        auto_promotion_allowed=False,
        auto_conflict_resolution_allowed=False,
        allowed_probe_scope="single_controlled_import_and_sandbox_query_probe_only",
        blocked_runtime_surfaces=(
            "network_sensitive_runtime_paths",
            "process_execution_sensitive_runtime_paths",
            "destructive_filesystem_runtime_paths",
            "canonical_memory_paths",
            "runtime_state_paths",
            "project_secret_paths",
        ),
        required_evidence_reports=(
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_risk_review_classification_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_integrity_security_report.json",
            "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_sandbox_smoke_report.json",
        ),
        approval_envelope_ready=approval_ready,
    )


def build_mempalace_real_backend_approval_envelope_preview() -> dict[str, object]:
    envelope = build_mempalace_real_backend_approval_envelope()

    return {
        "envelope_id": envelope.envelope_id,
        "hard_gate_passed": envelope.hard_gate_passed,
        "security_boundary_ready": envelope.security_boundary_ready,
        "classification_ready": envelope.classification_ready,
        "manual_security_review_required": envelope.manual_security_review_required,
        "manual_security_review_completed": envelope.manual_security_review_completed,
        "controlled_real_backend_probe_allowed": envelope.controlled_real_backend_probe_allowed,
        "full_real_backend_enablement_allowed": envelope.full_real_backend_enablement_allowed,
        "general_real_backend_query_allowed": envelope.general_real_backend_query_allowed,
        "network_allowed": envelope.network_allowed,
        "subprocess_allowed": envelope.subprocess_allowed,
        "shell_execution_allowed": envelope.shell_execution_allowed,
        "destructive_fs_allowed": envelope.destructive_fs_allowed,
        "secrets_access_allowed": envelope.secrets_access_allowed,
        "canonical_write_allowed": envelope.canonical_write_allowed,
        "runtime_mutation_allowed": envelope.runtime_mutation_allowed,
        "auto_promotion_allowed": envelope.auto_promotion_allowed,
        "auto_conflict_resolution_allowed": envelope.auto_conflict_resolution_allowed,
        "allowed_probe_scope": envelope.allowed_probe_scope,
        "blocked_runtime_surfaces": envelope.blocked_runtime_surfaces,
        "required_evidence_reports": envelope.required_evidence_reports,
        "approval_envelope_ready": envelope.approval_envelope_ready,
    }


def write_mempalace_real_backend_approval_envelope_report() -> Path:
    envelope = build_mempalace_real_backend_approval_envelope()
    _APPROVAL_REPORT.parent.mkdir(parents=True, exist_ok=True)

    payload = build_mempalace_real_backend_approval_envelope_preview()
    _APPROVAL_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not envelope.approval_envelope_ready:
        raise RuntimeError("MemPalace real backend approval envelope is not ready")

    return _APPROVAL_REPORT
