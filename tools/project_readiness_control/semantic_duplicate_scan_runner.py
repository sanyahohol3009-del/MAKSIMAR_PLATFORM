"""Semantic duplicate scan sub-runner.

This is a thin command wrapper around the existing root artifact semantic
duplicate preview surface. It does not implement a second semantic engine.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


_DEFAULT_TOOL_PATH = Path("tools/root_artifact_semantic_duplicate_preview.py")


@dataclass(frozen=True, slots=True)
class SemanticDuplicateScanRunResult:
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
        if not self.existing_tool_path:
            raise ValueError("existing_tool_path must not be empty")
        if "root_artifact_semantic_duplicate" not in " ".join(self.command):
            raise ValueError("semantic duplicate runner must call existing semantic surface")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")


def build_semantic_duplicate_scan_command(
    *,
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> tuple[str, ...]:
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    tool_path = str(existing_tool_path)
    if not tool_path:
        raise ValueError("existing_tool_path must not be empty")
    return (executable, tool_path, *tuple(extra_args))


def run_semantic_duplicate_scan(
    *,
    project_root: str | Path = ".",
    python_executable: str | None = None,
    existing_tool_path: str | Path = _DEFAULT_TOOL_PATH,
    extra_args: Sequence[str] = (),
) -> SemanticDuplicateScanRunResult:
    command = build_semantic_duplicate_scan_command(
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
    return SemanticDuplicateScanRunResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        existing_tool_path=str(existing_tool_path),
    )
