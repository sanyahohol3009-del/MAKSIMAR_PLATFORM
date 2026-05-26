from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingKind,
    RepositoryFindingSeverity,
    RepositoryScanEvidence,
    RepositoryScanFinding,
    SecretDetectionFinding,
)


def test_repository_secret_detection_contract_smoke() -> None:
    evidence = RepositoryScanEvidence(
        evidence_id="evidence_secret_001",
        source_path="EXTERNAL_BACKENDS/vendor/security_reports/vendor_detect_secrets_report.json",
        source_ref="line:1",
        scanner_id="detect_secrets",
    )
    finding = RepositoryScanFinding(
        finding_id="finding_secret_001",
        repository_id="vendor_repo",
        kind=RepositoryFindingKind.SECRET,
        severity=RepositoryFindingSeverity.CRITICAL,
        message="Verified secret was detected.",
        evidence=evidence,
        verified=True,
    )

    secret = SecretDetectionFinding(
        finding=finding,
        secret_kind="api_key",
        redacted_value="***REDACTED***",
    )

    assert secret.finding.verified is True
    assert secret.finding.kind is RepositoryFindingKind.SECRET


def test_repository_secret_detection_rejects_wrong_kind() -> None:
    evidence = RepositoryScanEvidence(
        evidence_id="evidence_license_001",
        source_path="EXTERNAL_BACKENDS/vendor/security_reports/license_report.json",
        source_ref="license",
        scanner_id="license_scan",
    )
    finding = RepositoryScanFinding(
        finding_id="finding_license_001",
        repository_id="vendor_repo",
        kind=RepositoryFindingKind.LICENSE,
        severity=RepositoryFindingSeverity.LOW,
        message="License finding.",
        evidence=evidence,
    )

    with pytest.raises(ValueError):
        SecretDetectionFinding(
            finding=finding,
            secret_kind="api_key",
            redacted_value="***REDACTED***",
        )
