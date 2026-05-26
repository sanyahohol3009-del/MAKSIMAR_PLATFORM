"""Batch-level readiness gate runner.

This runner composes existing readiness surfaces. It does not replace roadmap,
drift or stage guard tools.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from typing import Sequence

from tools.project_readiness_control.target_test_runner import (
    TargetTestRunResult,
    run_target_tests,
)


@dataclass(frozen=True, slots=True)
class BatchGateRunResult:
    batch_id: str
    readiness_command: tuple[str, ...]
    readiness_returncode: int
    readiness_stdout: str
    readiness_stderr: str
    target_result: TargetTestRunResult
    passed: bool
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id must not be empty")
        if not self.readiness_command:
            raise ValueError("readiness_command must not be empty")
        if not isinstance(self.target_result, TargetTestRunResult):
            raise TypeError("target_result must be TargetTestRunResult")
        if self.passed != (
            self.readiness_returncode == 0 and self.target_result.returncode == 0
        ):
            raise ValueError("passed must mirror readiness and target test return codes")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")


def build_readiness_map_command(
    batch_id: str,
    *,
    python_executable: str | None = None,
) -> tuple[str, ...]:
    if not batch_id:
        raise ValueError("batch_id must not be empty")
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (
        executable,
        "tools/project_readiness_control/project_file_readiness_map.py",
        "--batch-id",
        batch_id,
    )


def run_batch_gate(
    *,
    batch_id: str,
    target_paths: Sequence[str],
    python_executable: str | None = None,
) -> BatchGateRunResult:
    readiness_command = build_readiness_map_command(
        batch_id,
        python_executable=python_executable,
    )
    readiness = subprocess.run(
        readiness_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )
    target_result = run_target_tests(
        target_paths,
        python_executable=python_executable,
    )
    return BatchGateRunResult(
        batch_id=batch_id,
        readiness_command=readiness_command,
        readiness_returncode=readiness.returncode,
        readiness_stdout=readiness.stdout,
        readiness_stderr=readiness.stderr,
        target_result=target_result,
        passed=readiness.returncode == 0 and target_result.returncode == 0,
    )
