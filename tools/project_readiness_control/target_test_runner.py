"""Target pytest runner for project readiness control.

Target runs must stay quiet by default. Full-platform reports are explicitly
disabled here and are handled only by full_platform_auto_runner.py.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Mapping, Sequence


_FULL_REPORT_ENV = "MAKSIMAR_FULL_PLATFORM_REPORTS"
_FULL_REPORT_FLAG = "--maksimar-full-platform-reports"


@dataclass(frozen=True, slots=True)
class TargetTestRunResult:
    command: tuple[str, ...]
    target_paths: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    full_platform_reports_enabled: bool = False
    shell_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.command:
            raise ValueError("command must not be empty")
        if not self.target_paths:
            raise ValueError("target_paths must not be empty")
        if self.full_platform_reports_enabled:
            raise ValueError("target runner must not enable full-platform reports")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")
        if _FULL_REPORT_FLAG in self.command:
            raise ValueError("target runner must not use full-platform report flag")


def _clean_target_env(base_env: Mapping[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    env.pop(_FULL_REPORT_ENV, None)
    return env


def build_target_pytest_command(
    target_paths: Sequence[str],
    *,
    python_executable: str | None = None,
    pytest_args: Sequence[str] = ("-q",),
) -> tuple[str, ...]:
    if not target_paths:
        raise ValueError("target_paths must not be empty")
    normalized_targets = tuple(str(path) for path in target_paths)
    if any(not path or path.strip() != path for path in normalized_targets):
        raise ValueError("target paths must be non-empty and trimmed")
    if _FULL_REPORT_FLAG in pytest_args:
        raise ValueError("target pytest args must not include full-platform report flag")
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (executable, "-m", "pytest", *normalized_targets, *tuple(pytest_args))


def run_target_tests(
    target_paths: Sequence[str],
    *,
    python_executable: str | None = None,
    pytest_args: Sequence[str] = ("-q",),
    base_env: Mapping[str, str] | None = None,
) -> TargetTestRunResult:
    command = build_target_pytest_command(
        target_paths,
        python_executable=python_executable,
        pytest_args=pytest_args,
    )
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        env=_clean_target_env(base_env),
    )
    return TargetTestRunResult(
        command=command,
        target_paths=tuple(str(path) for path in target_paths),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
