from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.repository_risk_summary_builder import (
    build_repository_risk_summary,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    DependencyRiskFinding,
    RepositoryFindingKind,
    RepositoryFindingSeverity,
    RepositoryScanEvidence,
    RepositoryScanFinding,
    RepositoryScanResult,
    RepositoryScanSource,
)


def test_repository_dependency_risk_scan_contract_smoke() -> None:
    evidence = RepositoryScanEvidence(
        evidence_id="evidence_dependency_001",
        source_path="EXTERNAL_BACKENDS/vendor/security_reports/vendor_pip_audit_report.json",
        source_ref="CVE-0000-0001",
        scanner_id="pip_audit",
    )
    finding = RepositoryScanFinding(
        finding_id="finding_dependency_001",
        repository_id="vendor_repo",
        kind=RepositoryFindingKind.DEPENDENCY_RISK,
        severity=RepositoryFindingSeverity.HIGH,
        message="Dependency vulnerability detected.",
        evidence=evidence,
    )
    dependency = DependencyRiskFinding(
        finding=finding,
        package_name="demo-package",
        advisory_id="CVE-0000-0001",
    )
    result = RepositoryScanResult(
        repository_id="vendor_repo",
        source=RepositoryScanSource.VENDOR_SECURITY_GATE,
        findings=(dependency.finding,),
        scanner_ids=("pip_audit",),
        hard_gate_passed=False,
        manual_review_required=True,
    )

    summary = build_repository_risk_summary(result)

    assert summary.risk_level is RepositoryFindingSeverity.HIGH
    assert summary.dependency_risk_findings == 1
    assert summary.manual_review_required is True
