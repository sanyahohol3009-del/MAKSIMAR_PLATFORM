"""Read-only repository risk summary builder."""

from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingKind,
    RepositoryFindingSeverity,
    RepositoryScanResult,
)


_RISK_ORDER: dict[RepositoryFindingSeverity, int] = {
    RepositoryFindingSeverity.INFO: 0,
    RepositoryFindingSeverity.LOW: 1,
    RepositoryFindingSeverity.MEDIUM: 2,
    RepositoryFindingSeverity.HIGH: 3,
    RepositoryFindingSeverity.CRITICAL: 4,
}


@dataclass(frozen=True, slots=True)
class RepositoryRiskSummary:
    """Aggregated read-only repository risk summary."""

    repository_id: str
    risk_level: RepositoryFindingSeverity
    total_findings: int
    secret_findings: int
    license_findings: int
    dependency_risk_findings: int
    dangerous_script_findings: int
    verified_secret_count: int
    manual_review_required: bool
    hard_gate_passed: bool
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.repository_id:
            raise ValueError("repository_id must not be empty")
        if not isinstance(self.risk_level, RepositoryFindingSeverity):
            raise TypeError("risk_level must be RepositoryFindingSeverity")
        for field_name, value in (
            ("total_findings", self.total_findings),
            ("secret_findings", self.secret_findings),
            ("license_findings", self.license_findings),
            ("dependency_risk_findings", self.dependency_risk_findings),
            ("dangerous_script_findings", self.dangerous_script_findings),
            ("verified_secret_count", self.verified_secret_count),
        ):
            if value < 0:
                raise ValueError(f"{field_name} must not be negative")
        if not isinstance(self.evidence_ids, tuple):
            raise TypeError("evidence_ids must be a tuple")
        if self.total_findings == 0 and self.risk_level is not RepositoryFindingSeverity.INFO:
            raise ValueError("empty summary must have INFO risk level")
        if self.verified_secret_count > self.secret_findings:
            raise ValueError("verified_secret_count cannot exceed secret_findings")


def _highest_severity(result: RepositoryScanResult) -> RepositoryFindingSeverity:
    if not result.findings:
        return RepositoryFindingSeverity.INFO
    return max(
        (finding.severity for finding in result.findings),
        key=lambda severity: _RISK_ORDER[severity],
    )


def build_repository_risk_summary(
    result: RepositoryScanResult,
) -> RepositoryRiskSummary:
    """Build a deterministic read-only repository risk summary."""
    if not isinstance(result, RepositoryScanResult):
        raise TypeError("result must be RepositoryScanResult")

    return RepositoryRiskSummary(
        repository_id=result.repository_id,
        risk_level=_highest_severity(result),
        total_findings=len(result.findings),
        secret_findings=sum(
            1 for finding in result.findings if finding.kind is RepositoryFindingKind.SECRET
        ),
        license_findings=sum(
            1 for finding in result.findings if finding.kind is RepositoryFindingKind.LICENSE
        ),
        dependency_risk_findings=sum(
            1
            for finding in result.findings
            if finding.kind is RepositoryFindingKind.DEPENDENCY_RISK
        ),
        dangerous_script_findings=sum(
            1
            for finding in result.findings
            if finding.kind is RepositoryFindingKind.DANGEROUS_SCRIPT
        ),
        verified_secret_count=result.verified_secret_count,
        manual_review_required=result.manual_review_required,
        hard_gate_passed=result.hard_gate_passed,
        evidence_ids=tuple(finding.evidence.evidence_id for finding in result.findings),
    )
