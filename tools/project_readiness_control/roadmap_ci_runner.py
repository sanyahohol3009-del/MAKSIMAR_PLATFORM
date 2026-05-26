"""Roadmap CI sub-runner.

This wrapper reuses tools/foundation_roadmap_ci_check.py. It is not a second
roadmap validator.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


_DEFAULT_TOOL_PATH = Path("tools/foundation_roadmap_ci_check.py")


@dataclass(frozen=True, slots=True)
class RoadmapCiRunResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    existing_tool_path: str
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False
    shell_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.command:
            raise ValueError("command must not be empty")
        if "foundation_roadmap_ci_check.py" not in " ".join(self.command):
            raise ValueError("roadmap CI runner must call existing roadmap CI tool")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")


def build_roadmap_ci_command(
    *,
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> tuple[str, ...]:
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (executable, str(existing_tool_path), *tuple(extra_args))


def run_roadmap_ci(
    *,
    project_root: str | Path = ".",
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> RoadmapCiRunResult:
    command = build_roadmap_ci_command(
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
    return RoadmapCiRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        existing_tool_path=str(existing_tool_path),
    )
