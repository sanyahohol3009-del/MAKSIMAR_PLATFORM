"""Explicit full-platform pytest runner.

This runner is the only Batch 0.5 surface that enables full-platform reports.
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
class FullPlatformAutoRunResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    full_platform_reports_enabled: bool
    shell_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.command:
            raise ValueError("command must not be empty")
        if _FULL_REPORT_FLAG not in self.command:
            raise ValueError("full platform command must include report flag")
        if not self.full_platform_reports_enabled:
            raise ValueError("full_platform_reports_enabled must be true")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")


def build_full_platform_auto_command(
    *,
    python_executable: str | None = None,
    xdist_workers: str = "auto",
    extra_pytest_args: Sequence[str] = (),
) -> tuple[str, ...]:
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    if not xdist_workers:
        raise ValueError("xdist_workers must not be empty")
    return (
        executable,
        "-m",
        "pytest",
        "-q",
        "-n",
        xdist_workers,
        _FULL_REPORT_FLAG,
        *tuple(extra_pytest_args),
    )


def build_full_platform_auto_env(
    base_env: Mapping[str, str] | None = None,
) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    env[_FULL_REPORT_ENV] = "1"
    return env


def run_full_platform_auto(
    *,
    python_executable: str | None = None,
    xdist_workers: str = "auto",
    extra_pytest_args: Sequence[str] = (),
    base_env: Mapping[str, str] | None = None,
) -> FullPlatformAutoRunResult:
    command = build_full_platform_auto_command(
        python_executable=python_executable,
        xdist_workers=xdist_workers,
        extra_pytest_args=extra_pytest_args,
    )
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        env=build_full_platform_auto_env(base_env),
    )
    return FullPlatformAutoRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        full_platform_reports_enabled=True,
    )
