"""Repository quarantine policy for read-only repository scan contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from MAKSIMAR_CORE_LIB.security_layer.repository_risk_summary_builder import (
    RepositoryRiskSummary,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingSeverity,
)


class RepositoryQuarantineAction(str, Enum):
    ALLOW_READ_ONLY = "allow_read_only"
    REQUIRE_REVIEW = "require_review"
    QUARANTINE = "quarantine"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class RepositoryQuarantineDecision:
    """Repository quarantine decision.

    This is a policy decision model, not a runtime executor.
    """

    repository_id: str
    action: RepositoryQuarantineAction
    reason_codes: tuple[str, ...]
    allowed_for_read_only_reference: bool
    allowed_for_runtime: bool
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.repository_id:
            raise ValueError("repository_id must not be empty")
        if not isinstance(self.action, RepositoryQuarantineAction):
            raise TypeError("action must be RepositoryQuarantineAction")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.action is RepositoryQuarantineAction.BLOCK and self.allowed_for_runtime:
            raise ValueError("blocked repository cannot be allowed for runtime")
        if self.action is RepositoryQuarantineAction.QUARANTINE and self.allowed_for_runtime:
            raise ValueError("quarantined repository cannot be allowed for runtime")
        if self.action is RepositoryQuarantineAction.ALLOW_READ_ONLY and self.allowed_for_runtime:
            raise ValueError("read-only repository reference cannot allow runtime")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")


def evaluate_repository_quarantine(
    summary: RepositoryRiskSummary,
) -> RepositoryQuarantineDecision:
    """Evaluate repository quarantine decision from a read-only risk summary."""
    if not isinstance(summary, RepositoryRiskSummary):
        raise TypeError("summary must be RepositoryRiskSummary")

    if summary.verified_secret_count > 0 or summary.risk_level is RepositoryFindingSeverity.CRITICAL:
        return RepositoryQuarantineDecision(
            repository_id=summary.repository_id,
            action=RepositoryQuarantineAction.BLOCK,
            reason_codes=("critical_repository_risk",),
            allowed_for_read_only_reference=False,
            allowed_for_runtime=False,
        )

    if summary.risk_level is RepositoryFindingSeverity.HIGH:
        return RepositoryQuarantineDecision(
            repository_id=summary.repository_id,
            action=RepositoryQuarantineAction.QUARANTINE,
            reason_codes=("high_repository_risk",),
            allowed_for_read_only_reference=True,
            allowed_for_runtime=False,
        )

    if summary.manual_review_required or summary.risk_level is RepositoryFindingSeverity.MEDIUM:
        return RepositoryQuarantineDecision(
            repository_id=summary.repository_id,
            action=RepositoryQuarantineAction.REQUIRE_REVIEW,
            reason_codes=("manual_review_required",),
            allowed_for_read_only_reference=True,
            allowed_for_runtime=False,
        )

    return RepositoryQuarantineDecision(
        repository_id=summary.repository_id,
        action=RepositoryQuarantineAction.ALLOW_READ_ONLY,
        reason_codes=("repository_read_only_reference_allowed",),
        allowed_for_read_only_reference=True,
        allowed_for_runtime=False,
    )
