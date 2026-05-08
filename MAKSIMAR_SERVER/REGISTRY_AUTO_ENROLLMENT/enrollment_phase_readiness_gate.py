from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.auto_enroll_runner import (
    AutoEnrollmentDryRunResult,
    build_auto_enrollment_dry_run_result,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.enrollment_candidate_builder import (
    build_enrollment_candidate_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.enrollment_summary_builder import (
    build_auto_enrollment_summary,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.manifest_discovery import (
    build_manifest_discovery_contract,
)


_EXPECTED_PHASE_FLOW = (
    "manifest_discovery",
    "candidate_builder",
    "write_guard",
    "dry_run_runner",
    "registry_entry_ready",
    "dashboard_exposure_ready",
    "observability_binding_ready",
)


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RegistryAutoEnrollmentPhaseReadiness:
    """Final read-only readiness gate for PHASE 1.4.

    This contract proves that auto-enrollment can discover domains, build
    candidates, pass write guard, build dry-run result and expose a deterministic
    dashboard/observability-ready summary without writing files.
    """

    discovery_entries: int
    candidate_entries: int
    dry_run_entries: int
    summary_entries: int
    write_allowed_entries: int
    write_blocked_entries: int
    flow: tuple[str, ...]
    counts_consistent: bool
    flow_consistent: bool
    no_write_verified: bool
    write_guard_ready: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        discovery_entries = _ensure_non_negative_int(
            self.discovery_entries,
            "discovery_entries",
        )
        candidate_entries = _ensure_non_negative_int(
            self.candidate_entries,
            "candidate_entries",
        )
        dry_run_entries = _ensure_non_negative_int(
            self.dry_run_entries,
            "dry_run_entries",
        )
        summary_entries = _ensure_non_negative_int(
            self.summary_entries,
            "summary_entries",
        )
        write_allowed_entries = _ensure_non_negative_int(
            self.write_allowed_entries,
            "write_allowed_entries",
        )
        write_blocked_entries = _ensure_non_negative_int(
            self.write_blocked_entries,
            "write_blocked_entries",
        )

        if not self.flow:
            raise ValueError("flow must be non-empty")
        if tuple(self.flow) != _EXPECTED_PHASE_FLOW:
            raise ValueError("flow must match expected PHASE 1.4 flow")

        counts_consistent = _ensure_bool(self.counts_consistent, "counts_consistent")
        flow_consistent = _ensure_bool(self.flow_consistent, "flow_consistent")
        no_write_verified = _ensure_bool(self.no_write_verified, "no_write_verified")
        write_guard_ready = _ensure_bool(self.write_guard_ready, "write_guard_ready")
        phase_ready = _ensure_bool(self.phase_ready, "phase_ready")

        if dry_run_entries != write_allowed_entries + write_blocked_entries:
            raise ValueError("dry-run write guard counts must balance")

        if not counts_consistent:
            raise ValueError("counts_consistent must be True")
        if not flow_consistent:
            raise ValueError("flow_consistent must be True")
        if not no_write_verified:
            raise ValueError("no_write_verified must be True")
        if not write_guard_ready:
            raise ValueError("write_guard_ready must be True")
        if not phase_ready:
            raise ValueError("phase_ready must be True")

        object.__setattr__(self, "discovery_entries", discovery_entries)
        object.__setattr__(self, "candidate_entries", candidate_entries)
        object.__setattr__(self, "dry_run_entries", dry_run_entries)
        object.__setattr__(self, "summary_entries", summary_entries)
        object.__setattr__(self, "write_allowed_entries", write_allowed_entries)
        object.__setattr__(self, "write_blocked_entries", write_blocked_entries)


def build_registry_auto_enrollment_phase_readiness(
    project_root: Path | None = None,
    dry_run_result: AutoEnrollmentDryRunResult | None = None,
) -> RegistryAutoEnrollmentPhaseReadiness:
    """Build final PHASE 1.4 readiness gate without writing files."""

    root = project_root or Path.cwd()
    discovery = build_manifest_discovery_contract(root)
    candidates = build_enrollment_candidate_contract(root, discovery=discovery)
    result = dry_run_result or build_auto_enrollment_dry_run_result(root, candidates)
    summary = build_auto_enrollment_summary(root, result)

    summary_flow = tuple(summary["flow"])
    summary_entries = len(summary["entries"])

    counts_consistent = (
        discovery.total_entries
        == candidates.total_candidates
        == result.total_entries
        == int(summary["total_entries"])
        == summary_entries
    )

    flow_consistent = summary_flow == _EXPECTED_PHASE_FLOW
    no_write_verified = bool(result.dry_run and summary["dry_run"])
    write_guard_ready = (
        result.total_entries == result.write_allowed_entries + result.write_blocked_entries
    ) and all(
        entry.registry_entry_ready
        and entry.dashboard_exposure_ready
        and entry.observability_binding_ready
        for entry in result.entries
    )

    phase_ready = (
        counts_consistent
        and flow_consistent
        and no_write_verified
        and write_guard_ready
        and bool(summary["summary_ready"])
        and bool(result.run_ready)
    )

    return RegistryAutoEnrollmentPhaseReadiness(
        discovery_entries=discovery.total_entries,
        candidate_entries=candidates.total_candidates,
        dry_run_entries=result.total_entries,
        summary_entries=summary_entries,
        write_allowed_entries=result.write_allowed_entries,
        write_blocked_entries=result.write_blocked_entries,
        flow=summary_flow,
        counts_consistent=counts_consistent,
        flow_consistent=flow_consistent,
        no_write_verified=no_write_verified,
        write_guard_ready=write_guard_ready,
        phase_ready=phase_ready,
    )
