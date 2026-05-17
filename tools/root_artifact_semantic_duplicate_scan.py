from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_report_builder import (
    build_semantic_duplicate_report_from_paths,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only semantic duplicate report for MAKSIMAR root artifact hygiene."
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

    print(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
