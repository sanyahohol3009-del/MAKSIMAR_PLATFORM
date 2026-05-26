"""Project file readiness map tool.

This tool compares roadmap-expected files against the current repository tree.
It is read-only by default and writes JSON only when --output is explicitly used.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from MAKSIMAR_CORE_LIB.architecture_map.project_file_readiness_models import (  # noqa: E402
    ProjectBatchReadinessReport,
    build_project_batch_readiness_report,
)
from tools.project_readiness_control.roadmap_expected_files_registry import (  # noqa: E402
    get_expected_batch,
    list_expected_batches,
)


def build_readiness_reports(
    *,
    project_root: Path,
    batch_id: str | None = None,
) -> tuple[ProjectBatchReadinessReport, ...]:
    """Build file readiness reports for one batch or all registered batches."""
    batches = (
        (get_expected_batch(batch_id),)
        if batch_id
        else list_expected_batches()
    )

    return tuple(
        build_project_batch_readiness_report(
            batch_id=batch.batch_id,
            title=batch.title,
            expected_files=batch.expected_files,
            project_root=project_root,
        )
        for batch in batches
    )


def reports_to_payload(
    reports: tuple[ProjectBatchReadinessReport, ...],
) -> dict[str, object]:
    """Convert readiness reports to JSON-serializable payload."""
    ready = sum(1 for report in reports if report.status == "READY")
    partial = sum(1 for report in reports if report.status == "PARTIAL")
    missing = sum(1 for report in reports if report.status == "MISSING")

    return {
        "report_type": "project_file_readiness_map",
        "status": "READY" if partial == 0 and missing == 0 else "PARTIAL",
        "total_batches": len(reports),
        "ready_batches": ready,
        "partial_batches": partial,
        "missing_batches": missing,
        "reports": [report.to_dict() for report in reports],
    }


def render_text(payload: dict[str, object]) -> str:
    """Render a stable human-readable file readiness report."""
    lines = [
        "MAKSIMAR PROJECT FILE READINESS MAP",
        f"status={payload['status']}",
        f"total_batches={payload['total_batches']}",
        f"ready_batches={payload['ready_batches']}",
        f"partial_batches={payload['partial_batches']}",
        f"missing_batches={payload['missing_batches']}",
        "",
    ]

    for report in payload["reports"]:
        assert isinstance(report, dict)
        lines.append(f"PHASE/BATCH {report['batch_id']} — {report['title']}")
        lines.append(f"status={report['status']}")
        lines.append(f"files={report['existing_files']}/{report['total_files']}")

        missing_required = report["missing_required_files"]
        if missing_required:
            lines.append("missing_required_files:")
            for missing_path in missing_required:
                lines.append(f"- {missing_path}")

        lines.append("expected_files:")
        for entry in report["expected_files"]:
            assert isinstance(entry, dict)
            marker = "OK" if entry["status"] == "EXISTS" else "MISSING"
            lines.append(f"[{marker}] {entry['path']} ({entry['role']})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_json_payload(payload: dict[str, object], output_path: Path) -> None:
    """Write JSON payload to an explicit output path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build project file readiness map.")
    parser.add_argument(
        "--batch-id",
        default=None,
        help="Optional roadmap batch id, for example 0.1 or 0.4.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of text.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional JSON output path. Writes only when explicitly set.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reports = build_readiness_reports(
        project_root=PROJECT_ROOT,
        batch_id=args.batch_id,
    )
    payload = reports_to_payload(reports)

    if args.output:
        write_json_payload(payload, PROJECT_ROOT / args.output)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")

    return 0 if payload["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
