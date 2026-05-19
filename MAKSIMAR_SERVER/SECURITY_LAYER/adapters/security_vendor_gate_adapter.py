from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.security_layer.security_read_model import (
    SecurityAdapterReadModel,
    SecurityReadModelStatus,
)


@dataclass(frozen=True, slots=True)
class VendorGateSecuritySignal:
    backend_id: str
    official_remote_verified: bool
    commit_seen_in_remote_refs: bool
    canonical_memory_access: bool
    runtime_mutation_allowed: bool
    risky_static_findings_count: int
    dependency_vulnerabilities_count: int
    verified_secret_found: bool
    manual_security_review_required: bool

    def __post_init__(self) -> None:
        if not self.backend_id:
            raise ValueError("backend_id must not be empty")
        for field_name, value in (
            ("risky_static_findings_count", self.risky_static_findings_count),
            ("dependency_vulnerabilities_count", self.dependency_vulnerabilities_count),
        ):
            if value < 0:
                raise ValueError(f"{field_name} must not be negative")


@dataclass(frozen=True, slots=True)
class VendorGateAdapterDecision:
    backend_id: str
    allowed_for_runtime: bool
    allowed_for_read_only_reference: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.backend_id:
            raise ValueError("backend_id must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.allowed_for_runtime and self.reason_codes != ("vendor_gate_clean",):
            raise ValueError("runtime allowance requires clean vendor gate reason")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_read_model(self) -> SecurityAdapterReadModel:
        status = (
            SecurityReadModelStatus.HEALTHY
            if self.allowed_for_runtime
            else SecurityReadModelStatus.BLOCKED
        )
        return SecurityAdapterReadModel(
            adapter_id="security_vendor_gate_adapter",
            adapter_kind="vendor_gate_adapter",
            source_count=1,
            status=status,
            reason_codes=self.reason_codes,
        )


def evaluate_vendor_gate_signal(signal: VendorGateSecuritySignal) -> VendorGateAdapterDecision:
    reasons: list[str] = []

    if not signal.official_remote_verified:
        reasons.append("official_remote_not_verified")
    if not signal.commit_seen_in_remote_refs:
        reasons.append("commit_not_seen_in_remote_refs")
    if signal.canonical_memory_access:
        reasons.append("canonical_memory_access_forbidden")
    if signal.runtime_mutation_allowed:
        reasons.append("runtime_mutation_forbidden")
    if signal.risky_static_findings_count > 0:
        reasons.append("risky_static_findings_present")
    if signal.dependency_vulnerabilities_count > 0:
        reasons.append("dependency_vulnerabilities_present")
    if signal.verified_secret_found:
        reasons.append("verified_secret_found")
    if signal.manual_security_review_required:
        reasons.append("manual_security_review_required")

    if reasons:
        return VendorGateAdapterDecision(
            backend_id=signal.backend_id,
            allowed_for_runtime=False,
            allowed_for_read_only_reference=True,
            reason_codes=tuple(reasons),
        )

    return VendorGateAdapterDecision(
        backend_id=signal.backend_id,
        allowed_for_runtime=True,
        allowed_for_read_only_reference=True,
        reason_codes=("vendor_gate_clean",),
    )
