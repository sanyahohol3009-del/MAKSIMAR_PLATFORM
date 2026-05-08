from __future__ import annotations

from pathlib import Path
from typing import Dict

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.auto_enroll_runner import (
    AutoEnrollmentDryRunResult,
    build_auto_enrollment_dry_run_result,
)


_ENROLLMENT_PIPELINE_FLOW = (
    "manifest_discovery",
    "candidate_builder",
    "write_guard",
    "dry_run_runner",
    "registry_entry_ready",
    "dashboard_exposure_ready",
    "observability_binding_ready",
)


def build_auto_enrollment_summary(
    project_root: Path | None = None,
    dry_run_result: AutoEnrollmentDryRunResult | None = None,
) -> Dict[str, object]:
    """Build deterministic read-only summary for auto-enrollment pipeline."""
    selected_result = dry_run_result or build_auto_enrollment_dry_run_result(project_root)

    return {
        "flow": _ENROLLMENT_PIPELINE_FLOW,
        "total_entries": selected_result.total_entries,
        "write_allowed_entries": selected_result.write_allowed_entries,
        "write_blocked_entries": selected_result.write_blocked_entries,
        "dry_run": selected_result.dry_run,
        "run_ready": selected_result.run_ready,
        "entries": tuple(
            {
                "module_slug": entry.candidate.module_slug,
                "source_path": entry.candidate.source_path,
                "manifest_path": entry.candidate.manifest_path,
                "manifest_exists": entry.candidate.manifest_exists,
                "enrollment_action": entry.candidate.enrollment_action,
                "write_allowed": entry.write_guard.write_allowed,
                "write_reason": entry.write_guard.reason,
                "registry_entry_ready": entry.registry_entry_ready,
                "dashboard_exposure_ready": entry.dashboard_exposure_ready,
                "observability_binding_ready": entry.observability_binding_ready,
            }
            for entry in selected_result.entries
        ),
        "summary_ready": True,
    }
