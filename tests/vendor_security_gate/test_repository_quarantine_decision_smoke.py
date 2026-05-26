from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.repository_quarantine_policy import (
    RepositoryQuarantineAction,
    evaluate_repository_quarantine,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_risk_summary_builder import (
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


def test_repository_quarantine_blocks_verified_secret_smoke() -> None:
    evidence = RepositoryScanEvidence(
        evidence_id="evidence_secret_critical_001",
        source_path="EXTERNAL_BACKENDS/vendor/security_reports/vendor_detect_secrets_report.json",
        source_ref="secret:1",
        scanner_id="detect_secrets",
    )
    finding = RepositoryScanFinding(
        finding_id="finding_secret_critical_001",
        repository_id="vendor_repo",
        kind=RepositoryFindingKind.SECRET,
        severity=RepositoryFindingSeverity.CRITICAL,
        message="Verified secret detected.",
        evidence=evidence,
        verified=True,
    )
    result = RepositoryScanResult(
        repository_id="vendor_repo",
        source=RepositoryScanSource.VENDOR_SECURITY_GATE,
        findings=(finding,),
        scanner_ids=("detect_secrets",),
        hard_gate_passed=False,
        manual_review_required=True,
    )

    decision = evaluate_repository_quarantine(build_repository_risk_summary(result))

    assert decision.action is RepositoryQuarantineAction.BLOCK
    assert decision.allowed_for_runtime is False
    assert decision.allowed_for_read_only_reference is False
    assert decision.direct_execution_allowed is False


def test_repository_quarantine_allows_clean_read_only_reference_smoke() -> None:
    result = RepositoryScanResult(
        repository_id="vendor_repo",
        source=RepositoryScanSource.VENDOR_SECURITY_GATE,
        findings=(),
        scanner_ids=("vendor_security_gate",),
        hard_gate_passed=True,
        manual_review_required=False,
    )

    decision = evaluate_repository_quarantine(build_repository_risk_summary(result))

    assert decision.action is RepositoryQuarantineAction.ALLOW_READ_ONLY
    assert decision.allowed_for_read_only_reference is True
    assert decision.allowed_for_runtime is False
