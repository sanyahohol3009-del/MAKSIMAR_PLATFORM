from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_real_backend_security_boundary import (
    build_mempalace_real_backend_security_boundary_preview,
)

_VENDOR_GATE_REPORT = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json")
_RISK_REVIEW_REPORT = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_risk_review_classification_report.json")


@dataclass(frozen=True, slots=True)
class MemPalaceRiskFindingClassification:
    file: str
    kind: str
    detail: str
    category: str
    runtime_surface: str
    severity: str
    decision: str
    reason: str

    def __post_init__(self) -> None:
        for field_name in ("file", "kind", "detail", "category", "runtime_surface", "severity", "decision", "reason"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.decision not in {
            "excluded_vendor_test_surface",
            "excluded_vendor_benchmark_surface",
            "allowed_only_with_sandbox_boundary",
            "forbidden_for_real_backend_until_manual_review",
            "manual_review_required",
        }:
            raise ValueError(f"Unsupported decision: {self.decision}")


@dataclass(frozen=True, slots=True)
class MemPalaceRiskReviewClassificationReport:
    report_id: str
    total_findings: int
    classified_findings: int
    vendor_tests_findings: int
    vendor_benchmark_findings: int
    sandbox_allowed_findings: int
    forbidden_until_review_findings: int
    manual_review_findings: int
    production_surface_findings: int
    network_sensitive_findings: int
    subprocess_sensitive_findings: int
    destructive_fs_sensitive_findings: int
    pickle_sensitive_findings: int
    hard_gate_passed: bool
    manual_security_review_required: bool
    manual_security_review_completed: bool
    real_backend_enablement_allowed: bool
    real_backend_query_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    classification_ready: bool
    entries: Tuple[MemPalaceRiskFindingClassification, ...]

    def __post_init__(self) -> None:
        if self.total_findings != len(self.entries):
            raise ValueError("total_findings must match entries length")
        if self.classified_findings != self.total_findings:
            raise ValueError("all findings must be classified")
        if not self.hard_gate_passed:
            raise ValueError("hard_gate_passed must be True")
        if not self.manual_security_review_required:
            raise ValueError("manual_security_review_required must be True")
        if self.manual_security_review_completed:
            raise ValueError("manual_security_review_completed must be False in Batch 4B")
        if self.real_backend_enablement_allowed:
            raise ValueError("real_backend_enablement_allowed must be False in Batch 4B")
        if self.real_backend_query_allowed:
            raise ValueError("real_backend_query_allowed must be False in Batch 4B")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.classification_ready:
            raise ValueError("classification_ready must be True")


def _load_vendor_gate_report() -> dict[str, object]:
    if not _VENDOR_GATE_REPORT.exists():
        raise FileNotFoundError(f"vendor gate report missing: {_VENDOR_GATE_REPORT}")

    return json.loads(_VENDOR_GATE_REPORT.read_text(encoding="utf-8"))


def _classify_finding(raw: dict[str, object]) -> MemPalaceRiskFindingClassification:
    file = str(raw.get("file", "unknown"))
    kind = str(raw.get("kind", "unknown"))
    detail = str(raw.get("detail", "unknown"))

    file_lower = file.lower()
    detail_lower = detail.lower()

    if file_lower.startswith("tests/"):
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="vendor_test_surface",
            runtime_surface="excluded_from_maksimar_runtime",
            severity="review_info",
            decision="excluded_vendor_test_surface",
            reason="Finding is inside vendor tests and EXTERNAL_BACKENDS is excluded from MAKSIMAR pytest/runtime collection.",
        )

    if file_lower.startswith("benchmarks/"):
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="vendor_benchmark_surface",
            runtime_surface="excluded_from_maksimar_runtime",
            severity="review_info",
            decision="excluded_vendor_benchmark_surface",
            reason="Finding is inside vendor benchmarks and must not be used by MAKSIMAR runtime adapter.",
        )

    if any(token in detail_lower for token in ("urllib", "requests", "httpx", "socket", "ftplib", "paramiko")):
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="network_sensitive",
            runtime_surface="production_package_surface",
            severity="high_review",
            decision="forbidden_for_real_backend_until_manual_review",
            reason="Network-capable code requires explicit network policy review before real backend query execution.",
        )

    if "subprocess" in detail_lower or detail_lower in {"eval", "exec", "compile", "os.system"}:
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="process_execution_sensitive",
            runtime_surface="production_package_surface",
            severity="critical_review",
            decision="forbidden_for_real_backend_until_manual_review",
            reason="Process/shell execution is blocked by the MemPalace process boundary.",
        )

    if any(token in detail_lower for token in ("shutil.rmtree", "os.remove", "os.unlink")):
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="destructive_filesystem_sensitive",
            runtime_surface="production_package_surface",
            severity="critical_review",
            decision="forbidden_for_real_backend_until_manual_review",
            reason="Destructive filesystem operations are blocked outside sandbox_data.",
        )

    if "pickle" in detail_lower:
        return MemPalaceRiskFindingClassification(
            file=file,
            kind=kind,
            detail=detail,
            category="serialization_sensitive",
            runtime_surface="production_package_surface",
            severity="high_review",
            decision="allowed_only_with_sandbox_boundary",
            reason="Pickle usage can be unsafe with untrusted data and requires sandbox-only data policy.",
        )

    return MemPalaceRiskFindingClassification(
        file=file,
        kind=kind,
        detail=detail,
        category="uncategorized_sensitive",
        runtime_surface="unknown",
        severity="manual_review",
        decision="manual_review_required",
        reason="Finding requires manual classification before real backend enablement.",
    )


def build_mempalace_risk_review_classification_report() -> MemPalaceRiskReviewClassificationReport:
    gate = _load_vendor_gate_report()
    boundary = build_mempalace_real_backend_security_boundary_preview()

    raw_findings = gate.get("risky_static_findings", [])
    if not isinstance(raw_findings, list):
        raise ValueError("risky_static_findings must be a list")

    entries = tuple(_classify_finding(item) for item in raw_findings)

    vendor_tests_findings = sum(1 for entry in entries if entry.category == "vendor_test_surface")
    vendor_benchmark_findings = sum(1 for entry in entries if entry.category == "vendor_benchmark_surface")
    sandbox_allowed_findings = sum(1 for entry in entries if entry.decision == "allowed_only_with_sandbox_boundary")
    forbidden_until_review_findings = sum(
        1 for entry in entries if entry.decision == "forbidden_for_real_backend_until_manual_review"
    )
    manual_review_findings = sum(1 for entry in entries if entry.decision == "manual_review_required")
    production_surface_findings = sum(1 for entry in entries if entry.runtime_surface == "production_package_surface")

    network_sensitive_findings = sum(1 for entry in entries if entry.category == "network_sensitive")
    subprocess_sensitive_findings = sum(1 for entry in entries if entry.category == "process_execution_sensitive")
    destructive_fs_sensitive_findings = sum(1 for entry in entries if entry.category == "destructive_filesystem_sensitive")
    pickle_sensitive_findings = sum(1 for entry in entries if entry.category == "serialization_sensitive")

    total_findings = len(entries)

    classification_ready = (
        bool(gate["hard_gate_passed"])
        and bool(gate["manual_security_review_required"])
        and boundary["security_boundary_ready"] is True
        and boundary["real_backend_enablement_allowed"] is False
        and boundary["real_backend_query_allowed"] is False
        and boundary["canonical_write_allowed"] is False
        and boundary["runtime_mutation_allowed"] is False
        and total_findings == int(gate["risky_static_findings_count"])
        and total_findings == len(entries)
    )

    return MemPalaceRiskReviewClassificationReport(
        report_id="mempalace_risk_review_classification_001",
        total_findings=total_findings,
        classified_findings=len(entries),
        vendor_tests_findings=vendor_tests_findings,
        vendor_benchmark_findings=vendor_benchmark_findings,
        sandbox_allowed_findings=sandbox_allowed_findings,
        forbidden_until_review_findings=forbidden_until_review_findings,
        manual_review_findings=manual_review_findings,
        production_surface_findings=production_surface_findings,
        network_sensitive_findings=network_sensitive_findings,
        subprocess_sensitive_findings=subprocess_sensitive_findings,
        destructive_fs_sensitive_findings=destructive_fs_sensitive_findings,
        pickle_sensitive_findings=pickle_sensitive_findings,
        hard_gate_passed=bool(gate["hard_gate_passed"]),
        manual_security_review_required=bool(gate["manual_security_review_required"]),
        manual_security_review_completed=False,
        real_backend_enablement_allowed=False,
        real_backend_query_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        classification_ready=classification_ready,
        entries=entries,
    )


def build_mempalace_risk_review_classification_preview() -> Dict[str, object]:
    report = build_mempalace_risk_review_classification_report()

    return {
        "report_id": report.report_id,
        "classification_ready": report.classification_ready,
        "total_findings": report.total_findings,
        "classified_findings": report.classified_findings,
        "vendor_tests_findings": report.vendor_tests_findings,
        "vendor_benchmark_findings": report.vendor_benchmark_findings,
        "production_surface_findings": report.production_surface_findings,
        "network_sensitive_findings": report.network_sensitive_findings,
        "subprocess_sensitive_findings": report.subprocess_sensitive_findings,
        "destructive_fs_sensitive_findings": report.destructive_fs_sensitive_findings,
        "pickle_sensitive_findings": report.pickle_sensitive_findings,
        "sandbox_allowed_findings": report.sandbox_allowed_findings,
        "forbidden_until_review_findings": report.forbidden_until_review_findings,
        "manual_review_findings": report.manual_review_findings,
        "manual_security_review_required": report.manual_security_review_required,
        "manual_security_review_completed": report.manual_security_review_completed,
        "real_backend_enablement_allowed": report.real_backend_enablement_allowed,
        "real_backend_query_allowed": report.real_backend_query_allowed,
        "canonical_write_allowed": report.canonical_write_allowed,
        "runtime_mutation_allowed": report.runtime_mutation_allowed,
    }


def write_mempalace_risk_review_classification_report() -> Path:
    report = build_mempalace_risk_review_classification_report()
    _RISK_REVIEW_REPORT.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "report_id": report.report_id,
        "total_findings": report.total_findings,
        "classified_findings": report.classified_findings,
        "vendor_tests_findings": report.vendor_tests_findings,
        "vendor_benchmark_findings": report.vendor_benchmark_findings,
        "sandbox_allowed_findings": report.sandbox_allowed_findings,
        "forbidden_until_review_findings": report.forbidden_until_review_findings,
        "manual_review_findings": report.manual_review_findings,
        "production_surface_findings": report.production_surface_findings,
        "network_sensitive_findings": report.network_sensitive_findings,
        "subprocess_sensitive_findings": report.subprocess_sensitive_findings,
        "destructive_fs_sensitive_findings": report.destructive_fs_sensitive_findings,
        "pickle_sensitive_findings": report.pickle_sensitive_findings,
        "hard_gate_passed": report.hard_gate_passed,
        "manual_security_review_required": report.manual_security_review_required,
        "manual_security_review_completed": report.manual_security_review_completed,
        "real_backend_enablement_allowed": report.real_backend_enablement_allowed,
        "real_backend_query_allowed": report.real_backend_query_allowed,
        "canonical_write_allowed": report.canonical_write_allowed,
        "runtime_mutation_allowed": report.runtime_mutation_allowed,
        "classification_ready": report.classification_ready,
        "entries": [
            {
                "file": entry.file,
                "kind": entry.kind,
                "detail": entry.detail,
                "category": entry.category,
                "runtime_surface": entry.runtime_surface,
                "severity": entry.severity,
                "decision": entry.decision,
                "reason": entry.reason,
            }
            for entry in report.entries
        ],
    }

    _RISK_REVIEW_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return _RISK_REVIEW_REPORT
