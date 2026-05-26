"""Architecture X-Ray sub-runner.

This wrapper calls the existing tools/architecture_xray_radar.py surface.
It does not create a second X-Ray engine.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


_DEFAULT_TOOL_PATH = Path("tools/architecture_xray_radar.py")


@dataclass(frozen=True, slots=True)
class XrayRunResult:
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
        if "architecture_xray_radar.py" not in " ".join(self.command):
            raise ValueError("xray runner must call existing architecture_xray_radar.py")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")


def build_xray_command(
    *,
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> tuple[str, ...]:
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (executable, str(existing_tool_path), *tuple(extra_args))


def run_xray(
    *,
    project_root: str | Path = ".",
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> XrayRunResult:
    command = build_xray_command(
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
    return XrayRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        existing_tool_path=str(existing_tool_path),
    )
