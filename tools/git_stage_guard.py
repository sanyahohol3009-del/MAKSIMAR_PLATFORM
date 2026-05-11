from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable


FORBIDDEN_STAGED_PATTERNS = (
    r"^\.pymon$",
    r"^\.coverage$",
    r"^\.pytest_cache/",
    r"(^|/)__pycache__/",
    r"\.pyc$",
    r"(^|/)node_modules/",
    r"^EXTERNAL_BACKENDS/[^/]+/(source|venv|sandbox_data)(/|$)",
    r"^tests/runtime_core/",
)

GENERATED_WARNING_PATTERNS = (
    r"^\.pymon$",
    r"^\.coverage$",
    r"^EXTERNAL_BACKENDS/[^/]+/security_reports/vendor_.*\.json$",
)


@dataclass(frozen=True, slots=True)
class GuardResult:
    checked_files: tuple[str, ...]
    violations: tuple[str, ...]
    warnings: tuple[str, ...]
    passed: bool


def _git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def _matches(path: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, path) for pattern in patterns)


def get_staged_files() -> tuple[str, ...]:
    output = _git(["diff", "--cached", "--name-only"])
    if not output:
        return ()
    return tuple(line.strip() for line in output.splitlines() if line.strip())


def get_short_status_files() -> tuple[str, ...]:
    output = _git(["status", "--short"])
    if not output:
        return ()
    files: list[str] = []

    for line in output.splitlines():
        if len(line) >= 4:
            files.append(line[3:].strip())

    return tuple(files)


def check_files(files: tuple[str, ...]) -> GuardResult:
    violations: list[str] = []
    warnings: list[str] = []

    allow_runtime_core = os.environ.get("MAKSIMAR_ALLOW_RUNTIME_CORE_STAGE") == "1"

    for path in files:
        if path.startswith("tests/runtime_core/") and allow_runtime_core:
            continue

        if _matches(path, FORBIDDEN_STAGED_PATTERNS):
            violations.append(path)

        if _matches(path, GENERATED_WARNING_PATTERNS):
            warnings.append(path)

    return GuardResult(
        checked_files=files,
        violations=tuple(violations),
        warnings=tuple(warnings),
        passed=not violations,
    )


def print_result(result: GuardResult) -> None:
    print("===== MAKSIMAR GIT STAGE GUARD =====")
    print(f"checked_files: {len(result.checked_files)}")

    if result.warnings:
        print("warnings:")
        for item in result.warnings:
            print(f"  WARN: {item}")

    if result.violations:
        print("violations:")
        for item in result.violations:
            print(f"  BLOCKED: {item}")

    if result.passed:
        print("OK: git stage guard passed")
    else:
        print("ERROR: forbidden staged files detected")


def main() -> int:
    parser = argparse.ArgumentParser(description="MAKSIMAR git stage guard.")
    parser.add_argument("--staged", action="store_true", help="Check staged files.")
    parser.add_argument("--worktree-summary", action="store_true", help="Show worktree warning summary.")
    args = parser.parse_args()

    files = get_staged_files() if args.staged else get_short_status_files()
    result = check_files(files)
    print_result(result)

    if args.worktree_summary:
        worktree = get_short_status_files()
        warnings = tuple(path for path in worktree if _matches(path, GENERATED_WARNING_PATTERNS))
        if warnings:
            print("worktree generated warnings:")
            for item in warnings:
                print(f"  WARN: {item}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
