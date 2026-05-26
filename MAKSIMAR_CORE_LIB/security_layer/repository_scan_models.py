"""Repository scan contract models for MAKSIMAR vendor security gate.

This module defines canonical read-only models for repository scan findings.
It does not execute scans, does not import external backends, and does not
replace tools/vendor_security_gate.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class RepositoryFindingKind(str, Enum):
    SECRET = "secret"
    LICENSE = "license"
    DEPENDENCY_RISK = "dependency_risk"
    DANGEROUS_SCRIPT = "dangerous_script"
    STATIC_RISK = "static_risk"
    VENDOR_GATE = "vendor_gate"


class RepositoryFindingSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RepositoryScanSource(str, Enum):
    VENDOR_SECURITY_GATE = "vendor_security_gate"
    STATIC_CONTRACT = "static_contract"
    EXTERNAL_REPORT_REFERENCE = "external_report_reference"


_ALLOWED_RELATIVE_ROOTS = (
    "EXTERNAL_BACKENDS/",
    "MAKSIMAR_CORE_LIB/",
    "MAKSIMAR_SERVER/",
    "tools/",
    "tests/",
    "docs/",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be non-empty")


def _require_relative_path(value: str, field_name: str) -> None:
    _require_non_empty(value, field_name)
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"{field_name} must be repository-relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{field_name} must not contain empty/current/parent path parts")


def _require_allowed_path_root(value: str, field_name: str) -> None:
    _require_relative_path(value, field_name)
    if not value.startswith(_ALLOWED_RELATIVE_ROOTS):
        raise ValueError(
            f"{field_name} must start with one of {_ALLOWED_RELATIVE_ROOTS}, got {value!r}"
        )


@dataclass(frozen=True, slots=True)
class RepositoryScanEvidence:
    """Evidence reference for a repository scan finding."""

    evidence_id: str
    source_path: str
    source_ref: str
    scanner_id: str

    def __post_init__(self) -> None:
        _require_non_empty(self.evidence_id, "evidence_id")
        _require_allowed_path_root(self.source_path, "source_path")
        _require_non_empty(self.source_ref, "source_ref")
        _require_non_empty(self.scanner_id, "scanner_id")


@dataclass(frozen=True, slots=True)
class RepositoryScanFinding:
    """Canonical repository scan finding."""

    finding_id: str
    repository_id: str
    kind: RepositoryFindingKind
    severity: RepositoryFindingSeverity
    message: str
    evidence: RepositoryScanEvidence
    verified: bool = False
    false_positive: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.finding_id, "finding_id")
        _require_non_empty(self.repository_id, "repository_id")
        if not isinstance(self.kind, RepositoryFindingKind):
            raise TypeError("kind must be RepositoryFindingKind")
        if not isinstance(self.severity, RepositoryFindingSeverity):
            raise TypeError("severity must be RepositoryFindingSeverity")
        _require_non_empty(self.message, "message")
        if not isinstance(self.evidence, RepositoryScanEvidence):
            raise TypeError("evidence must be RepositoryScanEvidence")
        if self.verified and self.false_positive:
            raise ValueError("verified finding cannot be marked false_positive")


@dataclass(frozen=True, slots=True)
class SecretDetectionFinding:
    """Secret detection contract wrapper."""

    finding: RepositoryScanFinding
    secret_kind: str
    redacted_value: str

    def __post_init__(self) -> None:
        if not isinstance(self.finding, RepositoryScanFinding):
            raise TypeError("finding must be RepositoryScanFinding")
        if self.finding.kind is not RepositoryFindingKind.SECRET:
            raise ValueError("SecretDetectionFinding requires kind=SECRET")
        _require_non_empty(self.secret_kind, "secret_kind")
        _require_non_empty(self.redacted_value, "redacted_value")
        if "secret" in self.redacted_value.lower() and "***" not in self.redacted_value:
            raise ValueError("redacted_value must not expose raw secret-like values")


@dataclass(frozen=True, slots=True)
class LicenseFinding:
    """Repository license finding."""

    finding: RepositoryScanFinding
    license_id: str
    allowed: bool

    def __post_init__(self) -> None:
        if not isinstance(self.finding, RepositoryScanFinding):
            raise TypeError("finding must be RepositoryScanFinding")
        if self.finding.kind is not RepositoryFindingKind.LICENSE:
            raise ValueError("LicenseFinding requires kind=LICENSE")
        _require_non_empty(self.license_id, "license_id")


@dataclass(frozen=True, slots=True)
class DependencyRiskFinding:
    """Repository dependency risk finding."""

    finding: RepositoryScanFinding
    package_name: str
    advisory_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.finding, RepositoryScanFinding):
            raise TypeError("finding must be RepositoryScanFinding")
        if self.finding.kind is not RepositoryFindingKind.DEPENDENCY_RISK:
            raise ValueError("DependencyRiskFinding requires kind=DEPENDENCY_RISK")
        _require_non_empty(self.package_name, "package_name")
        _require_non_empty(self.advisory_id, "advisory_id")


@dataclass(frozen=True, slots=True)
class DangerousScriptFinding:
    """Dangerous script/static risk finding."""

    finding: RepositoryScanFinding
    script_path: str
    dangerous_call: str

    def __post_init__(self) -> None:
        if not isinstance(self.finding, RepositoryScanFinding):
            raise TypeError("finding must be RepositoryScanFinding")
        if self.finding.kind is not RepositoryFindingKind.DANGEROUS_SCRIPT:
            raise ValueError("DangerousScriptFinding requires kind=DANGEROUS_SCRIPT")
        _require_relative_path(self.script_path, "script_path")
        _require_non_empty(self.dangerous_call, "dangerous_call")


@dataclass(frozen=True, slots=True)
class RepositoryScanResult:
    """Canonical read-only repository scan result."""

    repository_id: str
    source: RepositoryScanSource
    findings: tuple[RepositoryScanFinding, ...]
    scanner_ids: tuple[str, ...]
    hard_gate_passed: bool
    manual_review_required: bool
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.repository_id, "repository_id")
        if not isinstance(self.source, RepositoryScanSource):
            raise TypeError("source must be RepositoryScanSource")
        if not isinstance(self.findings, tuple):
            raise TypeError("findings must be a tuple")
        if not isinstance(self.scanner_ids, tuple):
            raise TypeError("scanner_ids must be a tuple")
        if not self.scanner_ids:
            raise ValueError("scanner_ids must not be empty")
        if any(not isinstance(finding, RepositoryScanFinding) for finding in self.findings):
            raise TypeError("findings must contain RepositoryScanFinding entries")
        if any(finding.repository_id != self.repository_id for finding in self.findings):
            raise ValueError("all findings must match repository_id")
        if self.findings and self.hard_gate_passed:
            raise ValueError("hard_gate_passed cannot be true when findings are present")
        if any(
            finding.severity in {
                RepositoryFindingSeverity.HIGH,
                RepositoryFindingSeverity.CRITICAL,
            }
            for finding in self.findings
        ) and not self.manual_review_required:
            raise ValueError("high/critical findings require manual review")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    @property
    def verified_secret_count(self) -> int:
        return sum(
            1
            for finding in self.findings
            if finding.kind is RepositoryFindingKind.SECRET and finding.verified
        )

    @property
    def dependency_risk_count(self) -> int:
        return sum(
            1
            for finding in self.findings
            if finding.kind is RepositoryFindingKind.DEPENDENCY_RISK
        )

    @property
    def risky_static_findings_count(self) -> int:
        return sum(
            1
            for finding in self.findings
            if finding.kind in {
                RepositoryFindingKind.DANGEROUS_SCRIPT,
                RepositoryFindingKind.STATIC_RISK,
            }
        )
