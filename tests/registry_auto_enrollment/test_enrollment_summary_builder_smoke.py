from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_summary,
)


def test_enrollment_summary_builder_smoke() -> None:
    summary = build_auto_enrollment_summary()

    assert summary["summary_ready"] is True
    assert summary["dry_run"] is True
    assert summary["total_entries"] == len(summary["entries"])
    assert summary["flow"] == (
        "manifest_discovery",
        "candidate_builder",
        "write_guard",
        "dry_run_runner",
        "registry_entry_ready",
        "dashboard_exposure_ready",
        "observability_binding_ready",
    )
