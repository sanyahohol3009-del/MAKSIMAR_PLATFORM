"""Drift guard sub-runner.

This wrapper calls the existing roadmap post-step drift check. It does not
implement a second drift guard.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


_DEFAULT_TOOL_PATH = Path("tools/roadmap_post_step_drift_check.py")


@dataclass(frozen=True, slots=True)
class DriftGuardRunResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    existing_tool_path: str
    drift_check_passed: bool | None
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False
    shell_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.command:
            raise ValueError("command must not be empty")
        if "roadmap_post_step_drift_check.py" not in " ".join(self.command):
            raise ValueError("drift guard runner must call existing post-step drift check")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")


def _extract_drift_check_passed(stdout: str) -> bool | None:
    normalized = stdout.lower()
    if '"drift_check_passed": true' in normalized or "drift_check_passed=true" in normalized:
        return True
    if '"drift_check_passed": false' in normalized or "drift_check_passed=false" in normalized:
        return False
    return None


def build_drift_guard_command(
    *,
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> tuple[str, ...]:
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (executable, str(existing_tool_path), *tuple(extra_args))


def run_drift_guard(
    *,
    project_root: str | Path = ".",
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> DriftGuardRunResult:
    command = build_drift_guard_command(
        python_executable=python_executable,
        existing_tool_path=existing_tool_path,
        extra_args=extra_args,
    )
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        cwd=str(project_root),
    )
    return DriftGuardRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        existing_tool_path=str(existing_tool_path),
        drift_check_passed=_extract_drift_check_passed(completed.stdout),
    )
