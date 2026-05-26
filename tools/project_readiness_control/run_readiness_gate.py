"""CLI entrypoint for project readiness gate runners."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from tools.project_readiness_control.batch_gate_runner import run_batch_gate
from tools.project_readiness_control.full_platform_auto_runner import run_full_platform_auto


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run MAKSIMAR project readiness gate.")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--full-platform-auto", action="store_true")
    parser.add_argument("--xdist-workers", default="auto")
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    if args.full_platform_auto:
        result = run_full_platform_auto(xdist_workers=args.xdist_workers)
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return result.returncode

    if not args.target:
        raise SystemExit("--target is required unless --full-platform-auto is used")

    result = run_batch_gate(
        batch_id=args.batch_id,
        target_paths=tuple(args.target),
    )
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
