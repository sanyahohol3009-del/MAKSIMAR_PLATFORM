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

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_report_builder import (
    SemanticDuplicateReportReadModel,
    build_semantic_duplicate_report_from_paths,
)


@dataclass(frozen=True, slots=True)
class SemanticDuplicatePreviewReadModel:
    layer_id: str
    batch_id: str
    preview_id: str
    preview_kind: str
    scan_scope: str
    target_paths: tuple[str, ...]
    total_items: int
    true_duplicate_risk_count: int
    container_boundary_duplicate_allowed_count: int
    wrap_as_adapter_count: int
    keep_legacy_count: int
    migration_candidate_count: int
    create_new_count: int
    approval_required_count: int
    high_risk_count: int
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

        if self.preview_id != "semantic_duplicate_preview_v1":
            raise ValueError("preview_id must be semantic_duplicate_preview_v1")

        if self.preview_kind != "read_only_terminal_preview":
            raise ValueError("preview_kind must be read_only_terminal_preview")

        if not self.scan_scope:
            raise ValueError("scan_scope must not be empty")

        if not isinstance(self.target_paths, tuple):
            raise TypeError("target_paths must be a tuple")

        if not self.target_paths:
            raise ValueError("target_paths must not be empty")

        for target_path in self.target_paths:
            if not target_path:
                raise ValueError("target_paths must not contain empty values")
            if target_path.startswith("/"):
                raise ValueError("target_paths must be project-relative")
            if "\\" in target_path:
                raise ValueError("target_paths must use POSIX-style '/' separators")
            if ".." in Path(target_path).parts:
                raise ValueError("target_paths must not contain '..'")

        for field_name, value in (
            ("total_items", self.total_items),
            ("true_duplicate_risk_count", self.true_duplicate_risk_count),
            (
                "container_boundary_duplicate_allowed_count",
                self.container_boundary_duplicate_allowed_count,
            ),
            ("wrap_as_adapter_count", self.wrap_as_adapter_count),
            ("keep_legacy_count", self.keep_legacy_count),
            ("migration_candidate_count", self.migration_candidate_count),
            ("create_new_count", self.create_new_count),
            ("approval_required_count", self.approval_required_count),
            ("high_risk_count", self.high_risk_count),
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
        payload["target_paths"] = list(self.target_paths)
        payload["warnings"] = list(self.warnings)
        return payload


def build_semantic_duplicate_preview(
    report: SemanticDuplicateReportReadModel,
) -> SemanticDuplicatePreviewReadModel:
    return SemanticDuplicatePreviewReadModel(
        layer_id="ROOT_ARTIFACT_HYGIENE",
        batch_id="PHASE_0_BATCH_0_4",
        preview_id="semantic_duplicate_preview_v1",
        preview_kind="read_only_terminal_preview",
        scan_scope=report.scan_scope,
        target_paths=report.target_paths,
        total_items=report.total_items,
        true_duplicate_risk_count=report.true_duplicate_risk_count,
        container_boundary_duplicate_allowed_count=(
            report.container_boundary_duplicate_allowed_count
        ),
        wrap_as_adapter_count=report.wrap_as_adapter_count,
        keep_legacy_count=report.keep_legacy_count,
        migration_candidate_count=report.migration_candidate_count,
        create_new_count=report.create_new_count,
        approval_required_count=report.approval_required_count,
        high_risk_count=report.high_risk_count,
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


def collect_existing_project_paths(
    root: Path,
    *,
    max_files: int,
) -> tuple[str, ...]:
    ignored_parts = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "htmlcov",
        "node_modules",
        "project_audit",
        "venv",
    }

    paths: list[str] = []

    for path in sorted(root.rglob("*")):
        if len(paths) >= max_files:
            break

        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue

        if any(part in ignored_parts for part in relative_parts):
            continue

        if not path.is_file():
            continue

        paths.append(path.relative_to(root).as_posix())

    return tuple(paths)


def format_human_summary(preview: SemanticDuplicatePreviewReadModel) -> str:
    lines = [
        "===== ROOT ARTIFACT SEMANTIC DUPLICATE PREVIEW =====",
        f"layer_id: {preview.layer_id}",
        f"batch_id: {preview.batch_id}",
        f"scan_scope: {preview.scan_scope}",
        "",
        "Target paths:",
        *(f"  - {target_path}" for target_path in preview.target_paths),
        "",
        "Counts:",
        f"  total_items: {preview.total_items}",
        f"  true_duplicate_risk_count: {preview.true_duplicate_risk_count}",
        (
            "  container_boundary_duplicate_allowed_count: "
            f"{preview.container_boundary_duplicate_allowed_count}"
        ),
        f"  wrap_as_adapter_count: {preview.wrap_as_adapter_count}",
        f"  keep_legacy_count: {preview.keep_legacy_count}",
        f"  migration_candidate_count: {preview.migration_candidate_count}",
        f"  create_new_count: {preview.create_new_count}",
        f"  approval_required_count: {preview.approval_required_count}",
        f"  high_risk_count: {preview.high_risk_count}",
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
        description="Read-only semantic duplicate preview for MAKSIMAR root artifact hygiene."
    )
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument(
        "--target",
        action="append",
        required=True,
        help="Project-relative target path. Can be used multiple times.",
    )
    parser.add_argument(
        "--existing",
        action="append",
        default=[],
        help="Project-relative existing path. Can be used multiple times.",
    )
    parser.add_argument("--scan-scope", default="project")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument(
        "--format",
        choices=("json", "human"),
        default="human",
    )
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    existing_paths = tuple(args.existing) or collect_existing_project_paths(
        root,
        max_files=args.max_files,
    )

    report = build_semantic_duplicate_report_from_paths(
        target_paths=tuple(args.target),
        existing_paths=existing_paths,
        scan_scope=args.scan_scope,
    )
    preview = build_semantic_duplicate_preview(report)

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
