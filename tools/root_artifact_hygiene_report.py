from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_artifact_report_builder import (
    build_root_artifact_report_from_project_root,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only MAKSIMAR root artifact hygiene report."
    )
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    report = build_root_artifact_report_from_project_root(
        args.root,
        max_depth=args.max_depth,
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
