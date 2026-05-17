from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_artifact_report_builder import (
    RootArtifactReportReadModel,
    build_root_artifact_report_from_project_root,
)


@dataclass(frozen=True, slots=True)
class LocationValidationPreviewReadModel:
    layer_id: str
    batch_id: str
    preview_id: str
    preview_kind: str
    scanned_root: str
    total_items: int
    correct_location_count: int
    wrong_or_review_location_count: int
    archive_candidate_count: int
    correction_required_count: int
    approval_required_count: int
    source_count: int
    generated_count: int
    backup_count: int
    audit_report_count: int
    vendor_count: int
    unknown_count: int
    scan_readonly: bool
    delete_allowed: bool
    move_allowed: bool
    dashboard_safe: bool
    runtime_mutation_allowed: bool
    canonical_write_allowed: bool
    warnings: tuple[str, ...]
    next_action: str
    report: dict[str, Any]

    def __post_init__(self) -> None:
        if self.layer_id != "ROOT_ARTIFACT_HYGIENE":
            raise ValueError("layer_id must be ROOT_ARTIFACT_HYGIENE")

        if self.batch_id != "PHASE_0_BATCH_0_4":
            raise ValueError("batch_id must be PHASE_0_BATCH_0_4")

        if self.preview_id != "location_validation_preview_v1":
            raise ValueError("preview_id must be location_validation_preview_v1")

        if self.preview_kind != "read_only_terminal_preview":
            raise ValueError("preview_kind must be read_only_terminal_preview")

        if not self.scanned_root:
            raise ValueError("scanned_root must not be empty")

        if self.total_items < 0:
            raise ValueError("total_items must not be negative")

        for field_name, value in (
            ("correct_location_count", self.correct_location_count),
            ("wrong_or_review_location_count", self.wrong_or_review_location_count),
            ("archive_candidate_count", self.archive_candidate_count),
            ("correction_required_count", self.correction_required_count),
            ("approval_required_count", self.approval_required_count),
            ("source_count", self.source_count),
            ("generated_count", self.generated_count),
            ("backup_count", self.backup_count),
            ("audit_report_count", self.audit_report_count),
            ("vendor_count", self.vendor_count),
            ("unknown_count", self.unknown_count),
        ):
            if value < 0:
                raise ValueError(f"{field_name} must not be negative")

        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")

        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")

        if self.move_allowed:
            raise ValueError("move_allowed must remain false")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

        if not isinstance(self.warnings, tuple):
            raise TypeError("warnings must be a tuple")

        if not isinstance(self.report, dict):
            raise TypeError("report must be a dict")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["warnings"] = list(self.warnings)
        return payload


def build_location_validation_preview(
    report: RootArtifactReportReadModel,
) -> LocationValidationPreviewReadModel:
    return LocationValidationPreviewReadModel(
        layer_id="ROOT_ARTIFACT_HYGIENE",
        batch_id="PHASE_0_BATCH_0_4",
        preview_id="location_validation_preview_v1",
        preview_kind="read_only_terminal_preview",
        scanned_root=report.scanned_root,
        total_items=report.total_items,
        correct_location_count=report.correct_location_count,
        wrong_or_review_location_count=report.wrong_or_review_location_count,
        archive_candidate_count=report.archive_candidate_count,
        correction_required_count=report.correction_required_count,
        approval_required_count=report.approval_required_count,
        source_count=report.source_count,
        generated_count=report.generated_count,
        backup_count=report.backup_count,
        audit_report_count=report.audit_report_count,
        vendor_count=report.vendor_count,
        unknown_count=report.unknown_count,
        scan_readonly=report.scan_readonly,
        delete_allowed=report.delete_allowed,
        move_allowed=report.move_allowed,
        dashboard_safe=report.dashboard_safe,
        runtime_mutation_allowed=report.runtime_mutation_allowed,
        canonical_write_allowed=report.canonical_write_allowed,
        warnings=report.warnings,
        next_action=report.next_action,
        report=report.to_dict(),
    )


def format_human_summary(preview: LocationValidationPreviewReadModel) -> str:
    lines = [
        "===== ROOT ARTIFACT LOCATION VALIDATION PREVIEW =====",
        f"layer_id: {preview.layer_id}",
        f"batch_id: {preview.batch_id}",
        f"scanned_root: {preview.scanned_root}",
        "",
        "Counts:",
        f"  total_items: {preview.total_items}",
        f"  correct_location_count: {preview.correct_location_count}",
        f"  wrong_or_review_location_count: {preview.wrong_or_review_location_count}",
        f"  archive_candidate_count: {preview.archive_candidate_count}",
        f"  correction_required_count: {preview.correction_required_count}",
        f"  approval_required_count: {preview.approval_required_count}",
        "",
        "Artifact classes:",
        f"  source_count: {preview.source_count}",
        f"  generated_count: {preview.generated_count}",
        f"  backup_count: {preview.backup_count}",
        f"  audit_report_count: {preview.audit_report_count}",
        f"  vendor_count: {preview.vendor_count}",
        f"  unknown_count: {preview.unknown_count}",
        "",
        "Safety:",
        f"  scan_readonly: {preview.scan_readonly}",
        f"  delete_allowed: {preview.delete_allowed}",
        f"  move_allowed: {preview.move_allowed}",
        f"  dashboard_safe: {preview.dashboard_safe}",
        f"  runtime_mutation_allowed: {preview.runtime_mutation_allowed}",
        f"  canonical_write_allowed: {preview.canonical_write_allowed}",
        "",
        "Warnings:",
        *(f"  - {warning}" for warning in preview.warnings),
        "",
        f"next_action: {preview.next_action}",
    ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only location validation preview for MAKSIMAR root artifact hygiene."
    )
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument(
        "--format",
        choices=("json", "human"),
        default="human",
    )
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    report = build_root_artifact_report_from_project_root(
        Path(args.root),
        max_depth=args.max_depth,
    )
    preview = build_location_validation_preview(report)

    if args.format == "json":
        print(
            json.dumps(
                preview.to_dict(),
                ensure_ascii=False,
                indent=2 if args.pretty else None,
                sort_keys=True,
            )
        )
    else:
        print(format_human_summary(preview))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
