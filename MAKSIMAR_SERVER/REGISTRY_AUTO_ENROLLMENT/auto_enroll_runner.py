from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.enrollment_candidate_builder import (
    EnrollmentCandidate,
    EnrollmentCandidateContract,
    build_enrollment_candidate_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.enrollment_write_guard import (
    EnrollmentWriteGuardDecision,
    build_enrollment_write_guard_decision,
)


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class EnrollmentDryRunEntry:
    """Read-only dry-run entry for registry auto-enrollment."""

    candidate: EnrollmentCandidate
    write_guard: EnrollmentWriteGuardDecision
    registry_entry_ready: bool
    dashboard_exposure_ready: bool
    observability_binding_ready: bool

    def __post_init__(self) -> None:
        if not isinstance(self.registry_entry_ready, bool):
            raise ValueError("registry_entry_ready must be bool")
        if not isinstance(self.dashboard_exposure_ready, bool):
            raise ValueError("dashboard_exposure_ready must be bool")
        if not isinstance(self.observability_binding_ready, bool):
            raise ValueError("observability_binding_ready must be bool")
        if not self.registry_entry_ready:
            raise ValueError("registry_entry_ready must be True")
        if not self.dashboard_exposure_ready:
            raise ValueError("dashboard_exposure_ready must be True")
        if not self.observability_binding_ready:
            raise ValueError("observability_binding_ready must be True")


@dataclass(frozen=True, slots=True)
class AutoEnrollmentDryRunResult:
    """Read-only dry-run result for auto-enrollment."""

    total_entries: int
    write_allowed_entries: int
    write_blocked_entries: int
    dry_run: bool
    run_ready: bool
    entries: tuple[EnrollmentDryRunEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        write_allowed_entries = _ensure_non_negative_int(
            self.write_allowed_entries,
            "write_allowed_entries",
        )
        write_blocked_entries = _ensure_non_negative_int(
            self.write_blocked_entries,
            "write_blocked_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        computed_allowed = sum(
            1 for entry in self.entries if entry.write_guard.write_allowed
        )
        computed_blocked = sum(
            1 for entry in self.entries if not entry.write_guard.write_allowed
        )

        if write_allowed_entries != computed_allowed:
            raise ValueError("write_allowed_entries must match computed count")
        if write_blocked_entries != computed_blocked:
            raise ValueError("write_blocked_entries must match computed count")
        if total_entries != write_allowed_entries + write_blocked_entries:
            raise ValueError("write guard counts must balance")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be bool")
        if not self.dry_run:
            raise ValueError("dry_run must be True")
        if not isinstance(self.run_ready, bool):
            raise ValueError("run_ready must be bool")
        if not self.run_ready:
            raise ValueError("run_ready must be True")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "write_allowed_entries", write_allowed_entries)
        object.__setattr__(self, "write_blocked_entries", write_blocked_entries)


def build_auto_enrollment_dry_run_result(
    project_root: Path | None = None,
    candidates: EnrollmentCandidateContract | None = None,
) -> AutoEnrollmentDryRunResult:
    """Build auto-enrollment dry-run result without writing files."""
    root = project_root or Path.cwd()
    selected_candidates = candidates or build_enrollment_candidate_contract(root)

    entries = tuple(
        EnrollmentDryRunEntry(
            candidate=candidate,
            write_guard=build_enrollment_write_guard_decision(
                root / candidate.manifest_path,
                overwrite_existing=False,
            ),
            registry_entry_ready=True,
            dashboard_exposure_ready=True,
            observability_binding_ready=True,
        )
        for candidate in selected_candidates.candidates
    )

    return AutoEnrollmentDryRunResult(
        total_entries=len(entries),
        write_allowed_entries=sum(
            1 for entry in entries if entry.write_guard.write_allowed
        ),
        write_blocked_entries=sum(
            1 for entry in entries if not entry.write_guard.write_allowed
        ),
        dry_run=True,
        run_ready=True,
        entries=entries,
    )
