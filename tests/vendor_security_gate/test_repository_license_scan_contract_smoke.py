from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    LicenseFinding,
    RepositoryFindingKind,
    RepositoryFindingSeverity,
    RepositoryScanEvidence,
    RepositoryScanFinding,
)


def test_repository_license_scan_contract_smoke() -> None:
    evidence = RepositoryScanEvidence(
        evidence_id="evidence_license_001",
        source_path="EXTERNAL_BACKENDS/vendor/source/LICENSE",
        source_ref="license-file",
        scanner_id="license_scan",
    )
    finding = RepositoryScanFinding(
        finding_id="finding_license_001",
        repository_id="vendor_repo",
        kind=RepositoryFindingKind.LICENSE,
        severity=RepositoryFindingSeverity.MEDIUM,
        message="License requires review.",
        evidence=evidence,
    )

    license_finding = LicenseFinding(
        finding=finding,
        license_id="GPL-3.0",
        allowed=False,
    )

    assert license_finding.allowed is False
    assert license_finding.license_id == "GPL-3.0"
