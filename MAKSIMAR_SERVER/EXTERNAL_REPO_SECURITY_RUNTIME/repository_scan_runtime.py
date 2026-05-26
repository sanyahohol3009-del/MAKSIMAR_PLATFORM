"""Repository scan runtime facade.

This module does not execute repository scanners. It binds an already-produced
vendor gate payload to canonical repository scan contracts and existing server
security decisions.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.repository_quarantine_policy import (
    RepositoryQuarantineDecision,
    evaluate_repository_quarantine,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_risk_summary_builder import (
    RepositoryRiskSummary,
    build_repository_risk_summary,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingKind,
    RepositoryFindingSeverity,
    RepositoryScanEvidence,
    RepositoryScanFinding,
    RepositoryScanResult,
    RepositoryScanSource,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_vendor_gate_adapter import (
    VendorGateAdapterDecision,
    VendorGateSecuritySignal,
    evaluate_vendor_gate_signal,
)


_SECRET_SCANNERS = frozenset({"detect_secrets", "gitleaks", "trufflehog"})
_DEPENDENCY_SCANNERS = frozenset({"pip_audit", "osv_scanner", "grype"})
_DANGEROUS_STATIC_SCANNERS = frozenset({"bandit", "semgrep"})
_STATIC_RISK_SCANNERS = frozenset({"clamscan", "syft"})


_ALLOWED_PATH_MARKERS = (
    "EXTERNAL_BACKENDS/",
    "MAKSIMAR_CORE_LIB/",
    "MAKSIMAR_SERVER/",
    "tools/",
    "tests/",
    "docs/",
)


@dataclass(frozen=True, slots=True)
class RepositoryScanRuntimeEvaluation:
    """Read-only runtime evaluation for an external repository scan payload."""

    repository_id: str
    scan_result: RepositoryScanResult
    risk_summary: RepositoryRiskSummary
    quarantine_decision: RepositoryQuarantineDecision
    vendor_gate_decision: VendorGateAdapterDecision
    scanner_runtime_executed: bool = False
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.repository_id:
            raise ValueError("repository_id must not be empty")
        if not isinstance(self.scan_result, RepositoryScanResult):
            raise TypeError("scan_result must be RepositoryScanResult")
        if not isinstance(self.risk_summary, RepositoryRiskSummary):
            raise TypeError("risk_summary must be RepositoryRiskSummary")
        if not isinstance(self.quarantine_decision, RepositoryQuarantineDecision):
            raise TypeError("quarantine_decision must be RepositoryQuarantineDecision")
        if not isinstance(self.vendor_gate_decision, VendorGateAdapterDecision):
            raise TypeError("vendor_gate_decision must be VendorGateAdapterDecision")
        if self.repository_id != self.scan_result.repository_id:
            raise ValueError("repository_id must match scan_result.repository_id")
        if self.repository_id != self.risk_summary.repository_id:
            raise ValueError("repository_id must match risk_summary.repository_id")
        if self.repository_id != self.quarantine_decision.repository_id:
            raise ValueError("repository_id must match quarantine_decision.repository_id")
        if self.repository_id != self.vendor_gate_decision.backend_id:
            raise ValueError("repository_id must match vendor_gate_decision.backend_id")
        if self.scanner_runtime_executed:
            raise ValueError("repository scan runtime facade must not execute scanners")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")


def _require_mapping(payload: Mapping[str, Any]) -> None:
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")


def _string_value(payload: Mapping[str, Any], key: str, default: str = "") -> str:
    value = payload.get(key, default)
    if value is None:
        return default
    return str(value)


def _bool_value(payload: Mapping[str, Any], key: str, default: bool = False) -> bool:
    value = payload.get(key, default)
    if not isinstance(value, bool):
        raise TypeError(f"{key} must be a bool")
    return value


def _int_value(payload: Mapping[str, Any], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int):
        raise TypeError(f"{key} must be an int")
    if value < 0:
        raise ValueError(f"{key} must not be negative")
    return value


def _normalize_repository_path(value: str) -> str:
    normalized = value.replace("\\", "/").strip()

    for marker in _ALLOWED_PATH_MARKERS:
        marker_index = normalized.find(marker)
        if marker_index >= 0:
            return normalized[marker_index:]

    if normalized.startswith(_ALLOWED_PATH_MARKERS):
        return normalized

    name = PurePosixPath(normalized).name or "unknown"
    return f"EXTERNAL_BACKENDS/unknown/{name}"


def _join_repository_path(source_dir: str, relative_item: str) -> str:
    source_dir_normalized = _normalize_repository_path(source_dir or "EXTERNAL_BACKENDS/unknown")
    relative_normalized = relative_item.replace("\\", "/").strip().lstrip("/")

    if not relative_normalized:
        return source_dir_normalized

    if relative_normalized.startswith(_ALLOWED_PATH_MARKERS):
        return _normalize_repository_path(relative_normalized)

    return f"{source_dir_normalized.rstrip('/')}/{relative_normalized}"


def _scanner_finding_kind(scanner_name: str) -> RepositoryFindingKind:
    if scanner_name in _SECRET_SCANNERS:
        return RepositoryFindingKind.SECRET
    if scanner_name in _DEPENDENCY_SCANNERS:
        return RepositoryFindingKind.DEPENDENCY_RISK
    if scanner_name in _DANGEROUS_STATIC_SCANNERS:
        return RepositoryFindingKind.DANGEROUS_SCRIPT
    if scanner_name in _STATIC_RISK_SCANNERS:
        return RepositoryFindingKind.STATIC_RISK
    return RepositoryFindingKind.VENDOR_GATE


def _scanner_finding_severity(scanner_name: str) -> RepositoryFindingSeverity:
    if scanner_name in _SECRET_SCANNERS:
        return RepositoryFindingSeverity.CRITICAL
    if scanner_name in _DEPENDENCY_SCANNERS:
        return RepositoryFindingSeverity.HIGH
    if scanner_name in _DANGEROUS_STATIC_SCANNERS:
        return RepositoryFindingSeverity.HIGH
    if scanner_name == "clamscan":
        return RepositoryFindingSeverity.CRITICAL
    return RepositoryFindingSeverity.MEDIUM


def _scanner_returncode_indicates_finding(scanner_payload: Mapping[str, Any]) -> bool:
    returncode = scanner_payload.get("returncode")
    return returncode not in (0, None)


def _scanner_available(scanner_payload: Mapping[str, Any]) -> bool:
    available = scanner_payload.get("available", False)
    if not isinstance(available, bool):
        raise TypeError("scanner available must be bool")
    return available


def _build_evidence(
    *,
    repository_id: str,
    evidence_index: int,
    source_path: str,
    source_ref: str,
    scanner_id: str,
) -> RepositoryScanEvidence:
    return RepositoryScanEvidence(
        evidence_id=f"{repository_id}_evidence_{evidence_index:04d}",
        source_path=source_path,
        source_ref=source_ref,
        scanner_id=scanner_id,
    )


def _build_vendor_gate_finding(
    *,
    repository_id: str,
    evidence_index: int,
    source_dir: str,
    reason_code: str,
    severity: RepositoryFindingSeverity,
) -> RepositoryScanFinding:
    evidence = _build_evidence(
        repository_id=repository_id,
        evidence_index=evidence_index,
        source_path=_join_repository_path(source_dir, "vendor_gate_report.json"),
        source_ref=reason_code,
        scanner_id="vendor_security_gate",
    )
    return RepositoryScanFinding(
        finding_id=f"{repository_id}_vendor_gate_{evidence_index:04d}",
        repository_id=repository_id,
        kind=RepositoryFindingKind.VENDOR_GATE,
        severity=severity,
        message=f"Vendor gate reason: {reason_code}",
        evidence=evidence,
        verified=severity is RepositoryFindingSeverity.CRITICAL,
    )


def _build_static_finding(
    *,
    repository_id: str,
    evidence_index: int,
    source_dir: str,
    finding_payload: Mapping[str, Any],
) -> RepositoryScanFinding:
    file_name = str(
        finding_payload.get("file")
        or finding_payload.get("path")
        or finding_payload.get("filename")
        or "unknown.py"
    )
    call_name = str(
        finding_payload.get("call")
        or finding_payload.get("call_name")
        or finding_payload.get("function")
        or finding_payload.get("detail")
        or "dangerous_static_call"
    )
    line = str(finding_payload.get("line") or finding_payload.get("lineno") or "unknown")

    evidence = _build_evidence(
        repository_id=repository_id,
        evidence_index=evidence_index,
        source_path=_join_repository_path(source_dir, file_name),
        source_ref=f"line:{line};call:{call_name}",
        scanner_id="vendor_security_gate_static_ast",
    )

    return RepositoryScanFinding(
        finding_id=f"{repository_id}_dangerous_script_{evidence_index:04d}",
        repository_id=repository_id,
        kind=RepositoryFindingKind.DANGEROUS_SCRIPT,
        severity=RepositoryFindingSeverity.HIGH,
        message=f"Dangerous static call detected: {call_name}",
        evidence=evidence,
    )


def _build_scanner_result_finding(
    *,
    repository_id: str,
    evidence_index: int,
    source_dir: str,
    scanner_name: str,
    scanner_payload: Mapping[str, Any],
) -> RepositoryScanFinding:
    output_path = str(scanner_payload.get("output_path") or f"security_reports/{scanner_name}.json")
    returncode = scanner_payload.get("returncode")
    kind = _scanner_finding_kind(scanner_name)
    severity = _scanner_finding_severity(scanner_name)

    evidence = _build_evidence(
        repository_id=repository_id,
        evidence_index=evidence_index,
        source_path=_join_repository_path(source_dir, output_path),
        source_ref=f"{scanner_name}:returncode:{returncode}",
        scanner_id=scanner_name,
    )

    return RepositoryScanFinding(
        finding_id=f"{repository_id}_{scanner_name}_{evidence_index:04d}",
        repository_id=repository_id,
        kind=kind,
        severity=severity,
        message=f"{scanner_name} returned {returncode}",
        evidence=evidence,
        verified=kind is RepositoryFindingKind.SECRET,
    )


def _scanner_ids_from_payload(payload: Mapping[str, Any]) -> tuple[str, ...]:
    scanner_results = payload.get("scanner_results", {})
    if not isinstance(scanner_results, Mapping):
        raise TypeError("scanner_results must be a mapping")
    if scanner_results:
        return tuple(str(name) for name in scanner_results.keys())
    return ("vendor_security_gate",)


def build_repository_scan_result_from_vendor_gate_payload(
    payload: Mapping[str, Any],
) -> RepositoryScanResult:
    """Map an already-produced vendor gate payload to RepositoryScanResult."""
    _require_mapping(payload)

    repository_id = _string_value(payload, "vendor_name", "external_repository")
    if not repository_id:
        raise ValueError("vendor_name must not be empty")

    source_dir = _string_value(payload, "source_dir", "EXTERNAL_BACKENDS/unknown")
    scanner_results = payload.get("scanner_results", {})
    if not isinstance(scanner_results, Mapping):
        raise TypeError("scanner_results must be a mapping")

    findings: list[RepositoryScanFinding] = []
    evidence_index = 1

    risky_static_findings = payload.get("risky_static_findings", ())
    if not isinstance(risky_static_findings, (tuple, list)):
        raise TypeError("risky_static_findings must be a tuple or list")
    for item in risky_static_findings:
        if not isinstance(item, Mapping):
            raise TypeError("risky_static_findings entries must be mappings")
        findings.append(
            _build_static_finding(
                repository_id=repository_id,
                evidence_index=evidence_index,
                source_dir=source_dir,
                finding_payload=item,
            )
        )
        evidence_index += 1

    hard_blockers = payload.get("hard_blockers", ())
    if not isinstance(hard_blockers, (tuple, list)):
        raise TypeError("hard_blockers must be a tuple or list")
    for reason_code in hard_blockers:
        findings.append(
            _build_vendor_gate_finding(
                repository_id=repository_id,
                evidence_index=evidence_index,
                source_dir=source_dir,
                reason_code=str(reason_code),
                severity=RepositoryFindingSeverity.CRITICAL,
            )
        )
        evidence_index += 1

    for scanner_name_raw, scanner_payload_raw in scanner_results.items():
        scanner_name = str(scanner_name_raw)
        if not isinstance(scanner_payload_raw, Mapping):
            raise TypeError("scanner result entries must be mappings")
        if not _scanner_available(scanner_payload_raw):
            continue
        if not _scanner_returncode_indicates_finding(scanner_payload_raw):
            continue

        findings.append(
            _build_scanner_result_finding(
                repository_id=repository_id,
                evidence_index=evidence_index,
                source_dir=source_dir,
                scanner_name=scanner_name,
                scanner_payload=scanner_payload_raw,
            )
        )
        evidence_index += 1

    return RepositoryScanResult(
        repository_id=repository_id,
        source=RepositoryScanSource.VENDOR_SECURITY_GATE,
        findings=tuple(findings),
        scanner_ids=_scanner_ids_from_payload(payload),
        hard_gate_passed=_bool_value(payload, "hard_gate_passed", not findings),
        manual_review_required=(
            _bool_value(payload, "manual_security_review_required", False)
            or bool(findings)
        ),
    )


def build_vendor_gate_security_signal_from_repository_scan_result(
    *,
    result: RepositoryScanResult,
    payload: Mapping[str, Any],
) -> VendorGateSecuritySignal:
    """Build existing server vendor gate signal from canonical scan result."""
    if not isinstance(result, RepositoryScanResult):
        raise TypeError("result must be RepositoryScanResult")
    _require_mapping(payload)

    return VendorGateSecuritySignal(
        backend_id=result.repository_id,
        official_remote_verified=_bool_value(payload, "official_remote_verified", False),
        commit_seen_in_remote_refs=_bool_value(payload, "commit_seen_in_remote_refs", False),
        canonical_memory_access=_bool_value(payload, "canonical_memory_access", False),
        runtime_mutation_allowed=_bool_value(payload, "runtime_mutation_allowed", False),
        risky_static_findings_count=(
            result.risky_static_findings_count
            or _int_value(payload, "risky_static_findings_count", 0)
        ),
        dependency_vulnerabilities_count=(
            result.dependency_risk_count
            or _int_value(payload, "dependency_vulnerabilities_count", 0)
        ),
        verified_secret_found=result.verified_secret_count > 0,
        manual_security_review_required=(
            result.manual_review_required
            or _bool_value(payload, "manual_security_review_required", False)
        ),
    )


def evaluate_repository_scan_runtime_from_vendor_gate_payload(
    payload: Mapping[str, Any],
) -> RepositoryScanRuntimeEvaluation:
    """Evaluate repository scan runtime facade from an existing vendor gate payload."""
    scan_result = build_repository_scan_result_from_vendor_gate_payload(payload)
    risk_summary = build_repository_risk_summary(scan_result)
    quarantine_decision = evaluate_repository_quarantine(risk_summary)
    vendor_signal = build_vendor_gate_security_signal_from_repository_scan_result(
        result=scan_result,
        payload=payload,
    )
    vendor_gate_decision = evaluate_vendor_gate_signal(vendor_signal)

    return RepositoryScanRuntimeEvaluation(
        repository_id=scan_result.repository_id,
        scan_result=scan_result,
        risk_summary=risk_summary,
        quarantine_decision=quarantine_decision,
        vendor_gate_decision=vendor_gate_decision,
    )
